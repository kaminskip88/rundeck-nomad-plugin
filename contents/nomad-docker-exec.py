from rundeck_plugin_nomad import RundeckPluginNomad

plugin = RundeckPluginNomad(
    nomad_dc='str',
    nomad_constraints='list',
    nomad_priority='int',
    artifacts_artifacts='yaml',
    resources_disk='int',
    resources_cpu='int',
    resources_ram='int',
    docker_image='str',
    docker_user='str',
    docker_password='str',
    docker_exec_user='str',
    docker_command='str',
    docker_args='str',
    docker_script='str',
    docker_volumes='list',
    docker_env='dict'
)

log = plugin.logger(__name__)

plugin.nomad_connect(
    address=plugin.get_env('NOMAD_ADDR', prefix=''),
    region=plugin.get_env('NOMAD_REGION', prefix=''),
    timeout=5,
    secure=True
)

if plugin.config['docker_script']:
    job_tpls = [{
        'EmbeddedTmpl': plugin.config['docker_script'],
        'DestPath': 'local/script.sh'
    }]
else:
    job_tpls = []

job_conf = {
    'image': plugin.config['docker_image'],
    'command': plugin.config[
        'docker_command'] if not plugin.config['docker_script'] else 'sh',
    'args': plugin.config[
        'docker_args'].split() if not plugin.config[
            'docker_script'] else ['/local/script.sh'],
    'volumes': plugin.config['docker_volumes']
}
if plugin.config['docker_user']:
    job_conf['auth'] = {
        'username': plugin.config['docker_user'],
        'password': plugin.config['docker_password']
    }

plugin.nomad_run(
    eval_timeout=30,
    alloc_timeout=60,
    group_name='rundeck',
    task_name='docker',
    name='-'.join(('rundeck', plugin.get_env('JOB_ID'),
                  plugin.get_env('JOB_EXECID'))),
    dc=[plugin.config['nomad_dc']],
    priority=plugin.config['nomad_priority'],
    constraints=plugin.config['nomad_constraints'],
    driver='docker',
    disk=plugin.config['resources_disk'],
    cpu=plugin.config['resources_cpu'],
    ram=plugin.config['resources_ram'],
    env=plugin.config['docker_env'],
    user=plugin.config['docker_exec_user'],
    templates=job_tpls,
    config=job_conf,
    artifacts=plugin.config['artifacts_artifacts']
)
