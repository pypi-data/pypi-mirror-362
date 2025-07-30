import math
import inspect
import time
import sys
import subprocess
import shlex
import json
import uuid
import os
import datetime
import traceback
import enum
import sqlite3
import zoneinfo
from dataclasses import dataclass

import dotenv
import buelon.helpers.sqlite3_helper
import buelon.helpers.postgres

from cronevents.timezone_util import TimezoneConverter


dotenv.load_dotenv('.env')

# environment variables
USING_POSTGRES = os.environ.get('CRON_EVENTS_USING_POSTGRES', None) == 'true'
REGISTER_CRON_EVENT = os.environ.get('REGISTER_CRON_EVENT', None) == 'true'
REGISTER_VERBOSE_CRON_EVENT = os.environ.get('REGISTER_VERBOSE_CRON_EVENT', None) == 'true'
# LOG_CRON_EVENT_LOGS = os.environ.get('LOG_CRON_EVENT_LOGS', None) == 'true'  # here for reference. Used in event.py
LOG_CRON_EVENT_TRIGGERS = os.environ.get('LOG_CRON_EVENT_TRIGGERS', None) == 'true'

DEFAULT_DB = buelon.helpers.sqlite3_helper.Sqlite3(
    location=os.path.join('.cronevents', 'event_manager.db')
)
DAYS_OF_THE_WEEK = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

STARTING_TOKENS = ['every', 'in', 'on']


timezone_converter = TimezoneConverter()


def add_timezone_abbr(tz: str, abbr: str):
    # timezone_converter[tz] = abbr
    timezone_converter.add(tz, abbr)


class Tokens(enum.Enum):
    """
    Tokens for cron event syntax.
    """
    OR: str = '||'
    AT: str = '@'


class CronEventError(Exception):
    """
    Exception for cron event errors.
    """


class CronEventSyntaxError(CronEventError):
    """
    Exception for cron event syntax errors.
    """


def get_db():
    if USING_POSTGRES:
        return buelon.helpers.postgres.get_postgres_from_env()
    return DEFAULT_DB


def try_isnan(v):
    try:
        return math.isnan(v)
    except:
        return False


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def try_number(value, _type=float, on_fail_return_value=None, asignment=None, nan_allowed=False):
    try:
        v = _type(value)
        a = isinstance(asignment, list)
        if a:
            if len(asignment) < 1:
                asignment.append(v)
            else:
                asignment[0] = v
        if not nan_allowed and try_isnan(v):
            return on_fail_return_value
        return v if not a else True
    except:
        return on_fail_return_value


def query_at_time_syntax_checker(at: str):
    has_pm = False
    if 'am' in at:
        if 'pm' in at:
            raise CronEventSyntaxError('Only one am/pm is allowed')
        if not at.endswith('am'):
            raise CronEventSyntaxError('Invalid am format near `am`')
    if 'pm' in at:
        if not at.endswith('pm'):
            raise CronEventSyntaxError('Invalid pm format near `pm`')
        has_pm = True

    at = at.replace('am', '').replace('pm', '').strip()

    if at.count(':') > 2:
        raise CronEventSyntaxError('Invalid time format. Max use of `:` is 2')

    if at.count(':') == 2:
        hour, minute, second = at.split(':')
    elif at.count(':') == 1:
        hour, minute = at.split(':')
        second = '0'
    else:
        hour = at
        minute = '0'
        second = '0'

    try:
        hour = int(hour) + 12 if has_pm else int(hour)
        minute = int(minute)
        second = int(second)
    except ValueError:
        raise CronEventSyntaxError(f'Non-int value for time found: `{at}`')

    if 23 < hour < 0:
        raise CronEventSyntaxError(f'Invalid hour value: `{hour}`. Must be 23 < hour < 0')
    if 59 < minute < 0:
        raise CronEventSyntaxError(f'Invalid minute value: `{minute}`. Must be 59 < minute < 0')
    if 59 < second < 0:
        raise CronEventSyntaxError(f'Invalid second value: `{second}`. Must be 59 < second < 0')


def query_syntax_checker(query: str) -> None:
    if not isinstance(query, str):
        raise CronEventSyntaxError('Query must be a string')

    if '||' in query:
        queries = query.split('||')
        for q in queries:
            try:
                query_syntax_checker(q.strip())
            except CronEventSyntaxError as e:
                raise CronEventSyntaxError(f'Error in query `{q}`: {e}')
        return

    query, _ = get_time_zone(query)
    query = query.lower().strip()

    if not any(query.strip().startswith(f'{token} ') for token in STARTING_TOKENS):  # not query.strip().startswith('every'):
        raise CronEventSyntaxError('Query must start with one: ' + ', '.join(STARTING_TOKENS))

    for token in STARTING_TOKENS:
        if query.strip().startswith(f'{token} '):
            query = query.replace(f'{token} ', '', 1)
            break
    # query = query.replace('every', '').strip()

    if '@' in query:
        if query.count('@') > 1:
            raise CronEventSyntaxError('Only one @ is allowed')
        query, at = query.split('@')
        query_at_time_syntax_checker(at)

    for day in DAYS_OF_THE_WEEK:
        if day in query:
            if query.count(day) > 1:
                raise CronEventSyntaxError(f'Only one {day} is allowed')
            if '' != query.replace(day, '').strip():
                raise CronEventSyntaxError(f'Invalid format. Using day of the week cannot contain other values. (remove: `{query.replace(day, "")}` from `{query}`')
            else:
                return

    units = ['day', 'hour', 'minute', 'second']
    units += [f'{u}s' for u in units]
    tokens = [t.strip() for t in query.split()]
    if 'minus' in tokens:
        before_minus = tokens[:tokens.index('minus')]
        has_unit, has_number = False, False
        for token in before_minus:
            has_unit = has_unit or token in units
            if token in units:
                has_unit = True
            has_number = has_number or is_int(token)

        if not has_unit:
            raise CronEventSyntaxError(f'No unit found in before minus `{query}`')
        if not has_number:
            raise CronEventSyntaxError(f'No number found in before minus `{query}`')

        after_minus = tokens[tokens.index('minus') + 1:]
        has_unit, has_number = False, False
        for token in after_minus:
            has_unit = has_unit or token in units
            has_number = has_number or is_int(token)

        if not has_unit:
            raise CronEventSyntaxError(f'No unit found in after minus `{query}`')
        if not has_number:
            raise CronEventSyntaxError(f'No number found in after minus `{query}`')

        tokens.remove('minus')

    on_number = True

    for token in tokens:
        if on_number:
            if not is_int(token):
                raise CronEventSyntaxError(f'Expected number, got `{token}`')
            on_number = False
        else:
            if token not in units:
                raise CronEventSyntaxError(f'Expected unit, got `{token}`. Available units {", ".join(units)}')
            on_number = True

    if not on_number:
        raise CronEventSyntaxError(f'Expected unit, got end of query. Please add a unit or remove the last number. '
                                   f'Units: {", ".join(units)}')


def temp_file_name():
    if not os.path.exists('.cronevents'):
        os.makedirs('.cronevents')
    if not os.path.exists(os.path.join('.cronevents', 'temp')):
        os.makedirs(os.path.join('.cronevents', 'temp'))
    return os.path.join('.cronevents', 'temp', f'temp_{uuid.uuid4().hex}.json')


def temp_save_json(data):
    filename = temp_file_name()
    with open(filename, 'w') as f:
        json.dump(data, f)
    return filename


def invoke(event_id, module, func, args, kwargs):
    invoke_id = f'e{uuid.uuid1().hex}'
    script = '-c "import cronevents.event;cronevents.event.main()"'  # os.path.join(os.getcwd(), 'event.py')
    cmd = f'{sys.executable} {script} {invoke_id} {module} {func} {temp_save_json(args)} {temp_save_json(kwargs)}'
    print('running', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), module, func, invoke_id)  # , f'"{cmd}"')

    p = subprocess.Popen(
        shlex.split(cmd),
        env=dict(os.environ)
    )

    if LOG_CRON_EVENT_TRIGGERS:
        get_db().upload_table('cron_event_triggers', [{
            'id': invoke_id,
            'event_id': event_id,
            'pid': f'{p.pid}',
            'utc_time': datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc),  # datetime.datetime.fromtimestamp(time.time(), datetime.UTC),
            # 'epoch': time.time(),
            # 'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            # 'cmd': cmd,
            'module': module,
            'func': func,
            'args': json.dumps(args),
            'kwargs': json.dumps(kwargs),
        }], id_column='id')


def create_event(module, func, args, kwargs, query, override_last=None, override_id=None):
    get_db().upload_table('cronevents', [{
        'id': override_id if override_id is not None else f'{module}|{func}',
        'query': query,
        'last': override_last if override_last is not None else datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc),  # datetime.datetime.fromtimestamp(time.time(), datetime.UTC),
        'module': module,
        'func': func,
        'args': json.dumps(args),
        'kwargs': json.dumps(kwargs),
    }], id_column='id')


def edit_or_create_event(module=None, func=None, args=None, kwargs=None, query=None, last=None, override_id=None):
    if override_id is None and (module is None or func is None):
        raise ValueError('override_id must be specified if module and func are not specified')

    row = {'id': override_id if override_id is not None else f'{module}|{func}'}

    if module is not None:
        row['module'] = module
    if func is not None:
        row['func'] = func
    if args is not None:
        row['args'] = json.dumps(args)
    if kwargs is not None:
        row['kwargs'] = json.dumps(kwargs)
    if query is not None:
        row['query'] = query
    if last is not None:
        row['last'] = last

    get_db().upload_table('cronevents', [row], id_column='id')


def get_word_before_word(word: str, txt: str):
    if word not in txt:
        return ''
    return txt.split(word)[0].strip().split(' ')[-1].strip().split('\n')[-1].strip().split('\t')[-1].strip()


def parse_time(s: str):
    m = 0
    if 'minus' in s:
        m = parse_time(s.split('minus')[-1])
        s = s.split('minus')[0]
    v = 0
    if 'day' in s:
        x = try_number(get_word_before_word('day', s), on_fail_return_value=1.0)
        v += 86400 * x
    if 'hour' in s:
        x = try_number(get_word_before_word('hour', s), on_fail_return_value=1.0)
        v += 3600 * x
    if 'minute' in s:
        x = try_number(get_word_before_word('minute', s), on_fail_return_value=1.0)
        v += 60 * x
    if 'second' in s:
        x = try_number(get_word_before_word('second', s), on_fail_return_value=1.0)
        v += x
    return (v if v > 0 else 86400) - m


def parse_time_timedelta(s: str):
    def force_int(x):
        return try_number(x, _type=int, on_fail_return_value=0)

    def strip_list(l):
        return [x.strip() for x in l]

    query = s.split('@')[-1]
    q = query.lower().split('am')[0].split('pm')[0]

    if q.count(':') == 0:
        hr, _min, sec = force_int(q), 0, 0
    elif q.count(':') == 1:
        hr, _min = strip_list(q.split(':'))
        sec = 0
    elif q.count(':') == 2:
        hr, _min, sec = strip_list(q.split(':'))
    else:
        hr, _min, sec = 0, 0, 0

    if 'pm' in query.lower() and int(hr) < 12:
        hr = force_int(hr) + 12

    return datetime.timedelta(hours=force_int(hr), minutes=force_int(_min), seconds=force_int(sec))


def get_time_zone(query: str):
    query = query.strip().lower()

    for tz in zoneinfo.available_timezones():
        og_tz = tz
        tz = tz.lower()

        if og_tz in timezone_converter:
            # abbr = timezone_converter[og_tz].abbr.lower()
            for abbr in timezone_converter.get_abbrs(og_tz):
                abbr = abbr.lower()
                if query.endswith(abbr):
                    return query.rstrip(abbr), zoneinfo.ZoneInfo(og_tz)

        if query.endswith(tz):
            return query.rstrip(tz), zoneinfo.ZoneInfo(og_tz)

    return query, datetime.timezone.utc


def ready(row):
    try:
        if isinstance(row['last'], str):
            row['last'] = datetime.datetime.fromisoformat(row['last'])
        # print('ready', row)
        # t = row['time']
        # _type = row['type']

        query: str = row['query']

        if '||' in query:
            queries = query.split('||')
            for q in queries:
                if ready({**row, 'query': q.strip()}):
                    return True
            return False

        query, tz = get_time_zone(row['query'])
        tz: zoneinfo.ZoneInfo
        query: str = query.lower()

        last = (row['last'] + (row['last'].utcoffset() or datetime.timedelta(seconds=0))).timestamp()

        if any([d in query for d in DAYS_OF_THE_WEEK]):
            last = datetime.datetime.fromtimestamp(last, tz=tz)  # datetime.timezone.utc)
            now = datetime.datetime.fromtimestamp(time.time(), tz=tz)  # datetime.timezone.utc)
            if abs((now - last).days) < 5:  # can only run once a week
                return False
            if now.strftime('%A').lower() in query:
                if '@' in query:
                    t = parse_time_timedelta(query)
                    current_time = datetime.timedelta(
                        hours=now.hour,
                        minutes=now.minute,
                        seconds=now.second
                    )
                    return current_time >= t
                return True
            return False

        if '@' not in query:
            t = parse_time(row['query'])  # - 10.
            # print('t', t, time.time() - last)
            return time.time() - last > t
        else:  # _type == '@':
            time_to = parse_time(query.split('@')[0]) if any(
                query.lower().startswith(f'{token} ') for token in STARTING_TOKENS
            ) else 86400 - 30  # 'every' in query else 86400 - 30

            query = query.split('@')[-1]
            q = query.lower().split('am')[0].split('pm')[0]
            if q.count(':') == 0:
                hr, _min, sec = str(try_number(q, int, on_fail_return_value='0')).strip(), '0', '0'
            elif q.count(':') == 1:
                hr, _min, sec = tuple([*tuple(map(lambda s: s.strip(), q.split(':'))), '0'])
            elif q.count(':') == 2:
                hr, _min, sec = tuple(map(lambda s: s.strip(), q.split(':')))
            elif q.count(':') == 1:
                hr, _min, sec = tuple(q.split(':'))
            else:
                hr, _min, sec = '0', '0', '0'
            if 'pm' in query.lower() and int(hr) < 12:
                hr = str(int(hr) + 12)

            # force_zero = lambda x: f'0{x}' if len(x) == 1 else f'{x}'
            # hr, _min, sec = force_zero(hr), force_zero(_min), force_zero(sec)
            # time_to_execute = datetime.datetime.strptime(
            #     datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc).strftime('%Y-%m-%d') + f' {hr}:{_min}:{sec}',
            #     '%Y-%m-%d %H:%M:%S'
            # ).replace(tzinfo=datetime.timezone.utc)
            # # print('time_to_execute', time_to_execute, datetime.datetime.now(), time.time() - last, datetime.datetime.now().strftime('%Y-%m-%d') + f' {hr}:{_min}:{sec}')
            # days = math.floor((time_to-1) / 60 / 60 / 24)
            # datetime.datetime.fromtimestamp(last)
            # datetime.datetime.fromtimestamp(time.time())
            # enough_time_past = (datetime.datetime.fromtimestamp(time.time()) - datetime.timedelta(days=days)).date() > datetime.datetime.fromtimestamp(last).date()
            # return time_to_execute < datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc) and enough_time_past  # time.time() - last > time_to

            hr, _min, sec = f'{hr:0>2}', f'{_min:0>2}', f'{sec:0>2}'
            time_to_execute = datetime.datetime.strptime(
                datetime.datetime.fromtimestamp(time.time(), tz=tz).strftime('%Y-%m-%d') + f' {hr}:{_min}:{sec}',
                '%Y-%m-%d %H:%M:%S'
            ).replace(tzinfo=tz)

            days = math.floor((time_to - 1) / 60 / 60 / 24)

            last_dt = datetime.datetime.fromtimestamp(last, tz=tz)
            now_dt = datetime.datetime.fromtimestamp(time.time(), tz=tz)

            enough_time_past = (now_dt - datetime.timedelta(days=days)).date() > last_dt.date()
            return time_to_execute < now_dt and enough_time_past
    except Exception as e:
        print('error in ready', e)
        traceback.print_exc()
        return False

def run(row):
    event_id = row['id']
    module, func, args, kwargs = row['module'], row['func'], json.loads(row['args']), json.loads(row['kwargs'])
    invoke(event_id, module, func, args, kwargs)


def update(row):
    query = row['query']
    if query.lower().strip().startswith('every'):
        row['last'] = datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc)  # datetime.datetime.now(datetime.UTC)  # time.time()
        get_db().upload_table('cronevents', [row], id_column='id')
    elif any(query.lower().strip().startswith(pre) for pre in ['in', 'on', 'this', 'next']):
        get_db().query(f'delete from cronevents where id = \'{row["id"]}\'')


def event(query: str, module: str=None, func: str=None, args: list = None, kwargs: dict = None):
    def __func(f):
        nonlocal module, func
        if REGISTER_CRON_EVENT:
            query_syntax_checker(query)
            _module, _func = os.path.basename(inspect.getmodule(f).__file__).split('.')[0], f.__name__
            module, func = module if isinstance(module, str) else _module, func if isinstance(func, str) else _func

            db = get_db()
            try:
                vals = db.download_table(sql=f"select * from cronevents where module='{module}' and func='{func}'")
            except:
                vals = None

            if vals:
                print('modifying event', module, func)
                if query != vals[0]['query']:
                    vals[0]['last'] = datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc)
                vals[0]['query'] = query
                vals[0]['args'] = json.dumps(args or [])
                vals[0]['kwargs'] = json.dumps(kwargs or {})
                db.upload_table('cronevents', vals, id_column='id')
            else:
                print('adding event', module, func)
                create_event(module, func, args or [], kwargs or {}, query)
        return f
    return __func


def main():
    print('version 0.0.38-alpha7')
    while True:
        try:
            for row in get_db().download_table('cronevents'):
                try:
                    query_syntax_checker(row['query'])
                    if ready(row):
                        run(row)
                        update(row)
                except CronEventSyntaxError:
                    get_db().query(f'delete from cronevents where id = \'{row["id"]}\'')
        except buelon.helpers.postgres.psycopg2.errors.UndefinedTable:
            print('No events have been registered')
            time.sleep(10.)
        except sqlite3.OperationalError as e:
            if 'no such table: cronevents' not in str(e):
                raise
            print('No events have been registered')
        except Exception as e:
            print('error ->', e)
            traceback.print_exc()
        time.sleep(2.)


if __name__ == '__main__':
    main()












