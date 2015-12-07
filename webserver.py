import socket
import sys
import codecs
from bs4 import BeautifulSoup

PORT = int(sys.argv[1])
HOST = ''

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
# response_body = ''
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    req = []
    req = request.split('\r\n')
    for r in req:
        print r

    request_file = req[0].split();
    if len(request_file)!=0 and request_file[1][1:].endswith((".html")):
        response_body = codecs.open(request_file[1][1:], 'r').read()
        parsed_html = BeautifulSoup(response_body)

        table_content = parsed_html.new_tag('table')
        isHeader = 0
        for r in req:
            table_data = r.split(': ',1)
            # print table_data
            if(isHeader == 0):
                isHeader = 1
                table_row = parsed_html.new_tag('tr')
                table_content.append(table_row)
                table_data1 = parsed_html.new_tag('td')
                table_data1.string = 'Header'
                table_row.append(table_data1)
                table_data2 = parsed_html.new_tag('td')
                table_data2.string = table_data[0]
                table_row.append(table_data2)
            else:
                if len(table_data) >= 2:
                    table_row = parsed_html.new_tag('tr')
                    table_content.append(table_row)
                    table_data1 = parsed_html.new_tag('td')
                    table_data1.string = table_data[0]
                    table_row.append(table_data1)
                    table_data2 = parsed_html.new_tag('td')
                    table_data2.string = table_data[1]
                    table_row.append(table_data2)
        
        len_css = 0
        for css_link in parsed_html.find('head').find_all('link'):
            css_path = css_link.get('href')
            css = codecs.open(css_path, 'r').read()
            css_tag = parsed_html.new_tag('style')
            css_tag.string = css
            len_css = len(str(css))
            css_link.replaceWith(css_tag)
        parsed_html.body.append(table_content)

        # print parsed_html
        len_js = 0
        for js_link in parsed_html.find_all('script'):
            js_path = js_link.get('src')
            if js_path:
                js = codecs.open(js_path, 'r').read()
                js_tag = parsed_html.new_tag('script')
                js_tag.string = js
                len_js = len(str(js))
                # parsed_html.head.insert_before(js_tag)
                js_link.replaceWith(js_tag)
            # print parsed_html
        response_body = str(parsed_html)



        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(response_body)+len_css+len_js,
            'Connection': 'close',
        }

        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in \
                                                response_headers.iteritems())

        http_response = request
        client_connection.send(''.join('HTTP/1.1 200 OK'))
        client_connection.send(response_headers_raw)
        client_connection.send('\n')
        client_connection.send(''.join(response_body))
    else:
        client_connection.send(''.join('HTTP/1.1 403 Forbidden'))
    client_connection.close()
listen_socket.close();