import imaplib, email, os
import dateutil.parser, datetime

IMAP_SERVER = "imap.gmail.com"
IMAP_USR = "reports@larsmarketing.com"
IMAP_PW = "reports418"
REPORT_DL_PATH = '/home/ubuntu/dlreports/'

def getMsgs(servername="myimapserverfqdn"):
    usernm = getpass.getuser()
    passwd = getpass.getpass()
    subject = 'Your SSL Certificate'
    conn = imaplib.IMAP4_SSL(servername)
    conn.login(usernm,passwd)
    conn.select('Inbox')
    typ, data = conn.search(None,'(UNSEEN SUBJECT "%s")' % subject)
    for num in data[0].split():
        typ, data = conn.fetch(num,'(RFC822)')
        msg = email.message_from_string(data[0][1])
        typ, data = conn.store(num,'-FLAGS','\\Seen')
        yield msg

def getAttachment(msg,check):
    for part in msg.walk():
        if part.get_content_type() == 'application/octet-stream':
          if check(part.get_filename()):
            return part.get_payload(decode=1)


def dlAGEmailLog(lsSDates, force=False):
    conn = imaplib.IMAP4_SSL(IMAP_SERVER)

    try:
        (retcode, capabilities) = conn.login(IMAP_USR, IMAP_PW)
    except:
        print sys.exc_info()[1]
        sys.exit(1)

    conn.select('Inbox', readonly=1) # Select inbox or default namespace

    dtStartDate = max(sorted(lsSDates)[0], '20130701') ## DO NOT GO BACK BEYOND July 1, 2013
    dateSince = dateutil.parser.parse(dtStartDate).strftime("%d-%b-%Y")
    print dateSince

    #dateSince = (datetime.date.today() - datetime.timedelta(30)).strftime("%d-%b-%Y")
    (retcode, messages) = conn.search(None, '(SENTSINCE {0})'.format(dateSince), '(FROM {0})'.format("reporting@alphagraphicsseattle.com".strip()))


    #(retcode, messages) = conn.search(None, '(UNSEEN)')
    if retcode == 'OK':
        for num in messages[0].split(' '):
            print 'Processing :', num
            typ, data = conn.fetch(num,'(RFC822)')
            msg = email.message_from_string(data[0][1])
            dt = dateutil.parser.parse(msg['date'])

            payload = getAttachment(msg,lambda x: x.endswith('.xls'))
            if not payload:
                continue

            directory = REPORT_DL_PATH + "AGEmailedReports/"
            filename = directory + "%s_AGEmailed.xls" % dt.strftime("%Y%m%d")
            if not os.path.exists(directory):
                os.makedirs(directory)

            if not os.path.exists(filename):
                open(filename,'w').write(payload)
                print "Writing to %s" % filename
            else:
                print "%s already exists" % filename

            # typ, data = conn.store(num,'-FLAGS','\\Seen')
            # print typ, data
            # if typ == 'OK':
            #     print data,'\n',30*'-'
            #     print msg

    conn.close()

