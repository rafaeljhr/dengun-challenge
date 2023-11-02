# Dengun Challenge

### MD5 hash verification 

Hashing on Ubuntu: 
```
md5sum forcast_collector.py > md5sum.txt
```

Verifying forcast_collector.py checksums on Ubuntu:
```
md5sum -c md5sum.txt
```

Expected output: `forcast_collector.py: OK`