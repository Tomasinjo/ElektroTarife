### O orodju

Nov sistem obračuna omrežnine uporablja 5 tarif. Glede na spodnjo tabelo, orodje vrne:
- trenutni časovni blok (1-5)
- naslednji najcenejši časovni blok
- slovar časovnih blokov naslednjih 24 ur

.. za trenutni ali poljubni dan

![alt text](https://www.elektro-ljubljana.si/portals/0/elj-nov_tarifni_sistem.jpg)


### Uporaba

Objekt za trenutni čas:
```
>>> from elektro_tarife import ElektroTarife
>>> et = ElektroTarife()
```

Objekt za poljubni dan:
```
>>> from elektro_tarife import ElektroTarife
>>> et = ElektroTarife(datetime(2024, 7, 15))
```

Trenutni časovni blok:
```
>>> et.current
4
```

Prihodnji časovni bloki:
```
>>> pprint(et.future_windows)
{2: [datetime.datetime(2024, 7, 1, 7, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>),
     datetime.datetime(2024, 7, 1, 8, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>),
     datetime.datetime(2024, 7, 1, 9, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>),
     datetime.datetime(2024, 7, 1, 10, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>),
     datetime.datetime(2024, 7, 1, 11, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>),
     datetime.datetime(2024, 7, 1, 12, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>),
     datetime.datetime(2024, 7, 1, 13, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>)],
 3: [datetime.datetime(2024, 7, 1, 6, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>)],
 4: [datetime.datetime(2024, 7, 1, 0, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>),
     datetime.datetime(2024, 7, 1, 1, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>),
     datetime.datetime(2024, 7, 1, 2, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>),
     datetime.datetime(2024, 7, 1, 3, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>),
     datetime.datetime(2024, 7, 1, 4, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>),
     datetime.datetime(2024, 7, 1, 5, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>)]}
```


Naslednji najcenejši časovni blok:
```
>>> cheapest = et.next_cheapest()
>>> cheapest.window
4
>>> cheapest.start
datetime.datetime(2024, 7, 1, 0, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>)
>>> cheapest.stop
datetime.datetime(2024, 7, 1, 6, 0, tzinfo=<DstTzInfo 'Europe/Ljubljana' CEST+2:00:00 DST>)

```