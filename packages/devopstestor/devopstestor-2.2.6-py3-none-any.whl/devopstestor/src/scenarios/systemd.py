from log_manager import logging
log = logging.getLogger('scenario.systemD')


def create_service(systemd_provisionner, service_name, username, group, exec_start, init_contexte, composant_name=None, **kwarg):
    if composant_name is None:
        composant_name = service_name
    return systemd_provisionner.create_service(
        composant_name=composant_name,
        service_name=service_name,
        User=username,
        Group=group,
        ExecStart=exec_start
    )

def start(systemd_provisionner, init_contexte, service_name, **kwarg):
    """
    Lance un systemctl start <service_name>
    """
    result_out_tpml = "--- Systemctl start ---\n" \
    "--- Systemctl status ---\n{}"

    res, start_out = systemd_provisionner.service_control(
        service_name=service_name,
        action="start"
    )
    res2, sout = status(systemd_provisionner, init_contexte, service_name)
    return res and res2, result_out_tpml.format(start_out, sout)

def stop(systemd_provisionner, init_contexte, service_name):
    """
    Lance un systemctl stop <service_name>
    """
    return systemd_provisionner.service_control(
        service_name=service_name,
        action="stop"
    )
def status(systemd_provisionner, init_contexte, service_name):
    """
    Lance un systemctl status <service_name>
    """
    return systemd_provisionner.service_control(
        service_name=service_name,
        action="status"
    )
