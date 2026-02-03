def call(Map args=[:]) {
  def name = args.get('name', 'World')
  echo "Hello, ${name}! (from Groovy shared library)"
}
