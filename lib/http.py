def http_get_request(url = 'http://detectportal.firefox.com/'):
    from utime import sleep
    import socket # Used by HTML get request

    # Connecting to the host specified by the URL
    _, _, host, path = url.split('/', 3)        # Separate URL request
    addr = socket.getaddrinfo(host, 80)[0][-1]  # Get IP address of host
    s = socket.socket()                         # Initialise the socket
    s.connect(addr)                             # Try connecting to host address

    # Send HTTP request to the host with specific path
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))    
    sleep(1)                               # Sleep for a second
    rec_bytes = s.recv(10000)                   # Receve response
    print(rec_bytes)                            # Print the response
    s.close()                                   # Close connection