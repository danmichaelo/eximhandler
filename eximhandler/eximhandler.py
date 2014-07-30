import logging


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

        Format the record and send it to the specified addressees.
        """
        try:
            from subprocess import Popen, PIPE

            msg = self.format(record)

            p1 = Popen(["echo", "-e", "Subject: " + self.subject + "\n\n" + msg], stdout=PIPE)
            p2 = Popen([self.exim_path, "-odf", "-i", self.toaddr], stdin=p1.stdout, stdout=PIPE)
            p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
            output = p2.communicate()[0]

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)