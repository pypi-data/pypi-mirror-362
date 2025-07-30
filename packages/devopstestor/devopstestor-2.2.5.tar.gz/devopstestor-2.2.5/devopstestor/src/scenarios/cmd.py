def run(machine_provisionner, init_contexte, command):
    ret, out = machine_provisionner.get_machine_controller().run_cmd(command)
    return str(ret) == '0', out