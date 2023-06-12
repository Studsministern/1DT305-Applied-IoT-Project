def wifi_connect(ssid, password):
    from utime import sleep
    import network

    # Put modem on Station mode
    wlan = network.WLAN(network.STA_IF)

    print() # Print an empty line

    # Connect if not already connected to WiFi
    if not wlan.isconnected():
        print('Connecting to network...')

        # Activate network interface
        wlan.active(True)

        # set power mode to get WiFi power-saving off (if needed)
        wlan.config(pm = 0xa11140)
        wlan.connect(ssid, password)  # Your WiFi Credential

        # Check if it is connected otherwise wait
        print('Waiting for connection...', end='')
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            sleep(1)

    # Print the IP assigned by router
    ip = wlan.ifconfig()[0]
    print('Connected on {}\n'.format(ip))
    return ip 