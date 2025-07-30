import socket

from ipykernel.kernelbase import Kernel


SOCKET_ADDR = '127.0.0.1'
PORT = 8042


class DcsKernel(Kernel):
    implementation = 'DCS'
    implementation_version = '0.1'
    language_info = {
        'name': 'lua',
        'version': '5.1',
        'mimetype': 'text/plain',
        'file_extension': '.lua',
    }
    banner = 'DCS kernel.'

    def __init__(self, *args, **kwargs):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.settimeout(10)
        super().__init__(*args, **kwargs)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        try:
            self.udp.sendto(code.encode(), (SOCKET_ADDR, PORT))
            ret_val = self.udp.recv(64 * 1024).decode()
            status = 'ok'
        except socket.timeout:
            ret_val = f'<< Dcs connection timeout ({SOCKET_ADDR}:{PORT})>>'
            status = 'error'
        except KeyboardInterrupt:
            ret_val = '<< Interrupted >>'
            status = 'aborted'
        except Exception as e:
            ret_val = f'<< Other exception occurred: {type(e).__name__}: {e} >>'
            status = 'error'
        finally:
            if not silent:
                stream_content = {'name': 'stdout', 'text': ret_val}
                self.send_response(self.iopub_socket, 'stream', stream_content)
        return {
            'status': status,
            'execution_count': self.execution_count,  # The base class increments the execution count
            'payload': [],
            'user_expressions': {},
        }

    def do_shutdown(self, restart):
        self.udp.close()
        return {'status': 'ok', 'restart': restart}


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp

    IPKernelApp.launch_instance(kernel_class=DcsKernel)
