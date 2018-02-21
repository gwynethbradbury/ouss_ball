import eisitirio.app as app




from eisitirio.app import eisitiriodb as db

from eisitirio.database.admin_fee import AdminFee
from eisitirio.database.admin_fee_transaction_item import AdminFeeTransactionItem
from eisitirio.database.affiliation import Affiliation
from eisitirio.database.announcement import Announcement
from eisitirio.database.battels import Battels
from eisitirio.database.battels_transaction import BattelsTransaction
from eisitirio.database.card_transaction import CardTransaction
from eisitirio.database.college import College
from eisitirio.database.dietary_requirements import DietaryRequirements
from eisitirio.database.eway_transaction import EwayTransaction
from eisitirio.database.group_purchase_request import GroupPurchaseRequest
from eisitirio.database.generic_transaction_item import GenericTransactionItem
from eisitirio.database.log import Log
from eisitirio.database.photo import Photo
from eisitirio.database.postage import Postage
from eisitirio.database.postage_transaction_item import PostageTransactionItem
from eisitirio.database.purchase_group import PurchaseGroup
from eisitirio.database.statistic import Statistic
from eisitirio.database.ticket import Ticket
from eisitirio.database.ticket_transaction_item import TicketTransactionItem
from eisitirio.database.transaction import DummyTransaction
from eisitirio.database.transaction import FreeTransaction
from eisitirio.database.transaction import Transaction
from eisitirio.database.transaction_item import TransactionItem
from eisitirio.database.user import User
from eisitirio.database.voucher import Voucher
from eisitirio.database.waiting import Waiting
from eisitirio.database.roundup_donation import RoundupDonation

db.create_all()


c=[]
c.append(College("N/a"))
c.append(Affiliation("None"))
c.append(Affiliation("OUSS Member"))
c.append(Affiliation("OUSS Extended Comittee"))
c.append(Affiliation("Artist"))

for a in c:
    db.session.add(a)
    db.session.commit()






