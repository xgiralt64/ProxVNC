from proxmoxer import ProxmoxAPI

class ProxmoxConnection:
    _instance = None

    @classmethod
    def get(cls, setup_data=None):
        # Primera inicialització
        if cls._instance is None:
            if setup_data is None:
                raise RuntimeError("setup_data és necessari la primera vegada")

            cls._instance = ProxmoxAPI(
                setup_data.hostname,
                user=setup_data.user,
                password=setup_data.password,
                otp=setup_data.otp,
                verify_ssl=False,
                port=8006,
            )

        return cls._instance
