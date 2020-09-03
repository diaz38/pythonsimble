import framework
# unique to module
import re

class Module(framework.module):

    def __init__(self, params):
        framework.module.__init__(self, params)
        self.register_option('host', self.goptions['domain']['value'], 'yes', 'fully qualified target hostname')
        self.info = {
                     'Name': 'Age Analyzer Lookup',
                     'Author': 'Brendan Coles (bcoles[at]gmail.com)',
                     'Description': 'Attempts to guess the author\'s age using ageanalyzer.com.',
                     'Comments': []
                     }
   
    def module_run(self):
        host  = self.options['host']['value']

        # request the author's age
        url = 'http://ageanalyzer.com/?url=%s' % (host)
        self.verbose('URL: %s' % url)
        try: resp = self.request(url)
        except KeyboardInterrupt:
            print ''
            return
        except Exception as e:
            self.error(e.__str__())
            return

        # extract and present results
        content = resp.text
        result = re.search(r'written by someone <strong>(.+)<\/strong> years old', content)
        if result:
            self.output('Ageanalyzer.com believes the author of %s to be %s years old.' % (host, result.group(1)))
        else:
            self.output('Ageanalyzer.com was unable to determine the age of the author.')