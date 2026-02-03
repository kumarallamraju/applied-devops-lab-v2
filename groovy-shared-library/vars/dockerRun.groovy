def call(Map args=[:]) {
  def image = args.image
  def cmd = args.cmd
  def mounts = args.get('mounts', [])
  def workdir = args.get('workdir', '/work')
  def network = args.get('network', '')

  if (!image || !cmd) {
    error('dockerRun requires: image, cmd')
  }

  def cmdB64 = cmd.getBytes('UTF-8').encodeBase64().toString()
  def mntArgs = mounts.collect { m -> "-v "${m}"" }.join(' ')
  def netArg = network ? "--network ${network}" : ""

  // Runs the base64-encoded script inside the target container.
  sh("docker run --rm ${netArg} ${mntArgs} -w ${workdir} -e CMD_B64='${cmdB64}' ${image} bash -lc "echo \\$CMD_B64 | base64 -d | bash"")
}
