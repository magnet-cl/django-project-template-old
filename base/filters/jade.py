from compressor.filters import CompilerFilter


class JadeCompilerFilter(CompilerFilter):
    bin_path = 'node_modules/jade-namespace/bin/jade-namespace'
    args = '{infile} -o {outfile}'
    command = '{} {}'.format(bin_path, args)

    options = (
        ("bin_path", bin_path),
    )

    def __init__(self, content, command=None, *args, **kwargs):
        # we expect the src to be within the templates folder and .jade
        # {u'src': u'/static/templates/test.jade', u'type': u'text/jade'}
        name = command[u'src'][18:-5]
        command = '{} --name {}'.format(self.command, name)
        super(JadeCompilerFilter, self).__init__(content, command, *args,
                                                 **kwargs)
