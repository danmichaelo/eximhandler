import logging
from subprocess import Popen, PIPE


class EximHandler(logging.Handler):
    """
    A handler class which sends an email using exim for each logging event.
    """
    def __init__(self, toaddr, subject, exim_path="/usr/sbin/exim"):
        """
        Initialize the handler.
        """
        logging.Handler.__init__(self)
        self.toaddr = toaddr
        self.subject = subject
        self.exim_path = exim_path

    def getSubject(self, record):
        """
        Determine the subject for the email.

        If you want to specify a subject line which is record-dependent,
        override this method.
        """
        return self.subject

    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified address.
        """
        body = self.format(record)
        try:
            proc1 = Popen(
                ['echo', '-e', 'Subject: %s\n\n%s' % (self.subject, body)],
                stdout=PIPE
            )

            proc2 = Popen(
                [self.exim_path, '-odf', '-i', self.toaddr],
                stdin=proc1.stdout, stdout=PIPE
            )

            # Allow proc1 to receive a SIGPIPE if proc2 exits.
            proc1.stdout.close()

            # Wait for proc2 to exit
            proc2.communicate()

        except (KeyboardInterrupt, SystemExit):
            raise

        except Exception:
            self.handleError(record)
