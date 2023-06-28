import asyncio

from lnbits.core.models import Payment
from lnbits.helpers import get_current_extension_name
from lnbits.tasks import register_invoice_listener

from .views_api import api_ticket_send_ticket


async def wait_for_paid_invoices():
    invoice_queue = asyncio.Queue()
    register_invoice_listener(invoice_queue, get_current_extension_name())

    while True:
        payment = await invoice_queue.get()
        await on_invoice_paid(payment)


async def on_invoice_paid(payment: Payment) -> None:
    # (avoid loops)
    if (
        payment.extra
        and "bookie" == payment.extra.get("tag")
        and payment.extra.get("reward_target")
    ):
        await api_ticket_send_ticket(
            payment.memo,
            payment.payment_hash,
        )
    return
