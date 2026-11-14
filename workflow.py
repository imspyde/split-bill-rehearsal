from dataclasses import dataclass

from dagflows.authoring import Workflow
from dagflows.runtime import Ctx

wf = Workflow("split-bill")


@dataclass
class Bill:
    amount: float
    tip_percent: float
    people: int


new_bill = wf.trigger("new_bill", event=Bill)


@wf.node(depends=[new_bill])
def split_bill(bill: Bill, ctx: Ctx) -> dict:
    total = bill.amount + (bill.amount * bill.tip_percent / 100)
    per_person = total / bill.people

    ctx.log.info(f"Total: {total:,.0f}; per person: {per_person:,.0f}")

    return {"total": total, "per_person": per_person}
