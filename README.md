# Custom Calendar Creator demo project

See [the main repo](https://github.com/beyarkay/c3) for details

## YAML calendar format

It is expected that the calendar files (by default matching `calendars/*.yaml`)
have a specific format:

1. Each file in `calendars/` will be turned into a single ICS file with the
   same name but with the extension `.ics`. So `calendars/simple-calendar.yaml`
   will become `calendars/simple-calendar.ics`. These `.ics` files will then be
   published.

   If you want multiple calendars, create multiple YAML files.

2. Each `.yaml` file should contain a list under the key `events`. Other keys
   may be added in the future.

3. Each of the items in the `events` list should be a single event, with
   different keys and values which will be mapped to single calendar events.

For example, this will create a single calendar with one event:

```yaml
events:
  - start: 2022-01-01T08:00:00.0000
    end: 2022-01-01T10:00:00.0000
    title: 'Happy new year!',
    description: 'This event was created by [c3](https://github.com/beyarkay/c3)',
```
