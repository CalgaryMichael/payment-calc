from payment_calc.models import outcome as under_test


def test_outcome__outstanding_debt__no_debts():
    model = under_test.Outcome(
        effective_date=None,
        debt_outcomes=[]
    )
    assert model.outstanding_debt() is False


def test_outcome__outstanding_debt__with_no_outstanding_debts():
    model = under_test.Outcome(
        effective_date=None,
        debt_outcomes=[
            under_test.DebtOutcome(debt_name='jazz', debt_total=0.00)
        ]
    )
    assert model.outstanding_debt() is False


def test_outcome__outstanding_debt__with_outstanding_debts():
    model = under_test.Outcome(
        effective_date=None,
        debt_outcomes=[
            under_test.DebtOutcome(debt_name='jazz', debt_total=1000.00)
        ]
    )
    assert model.outstanding_debt() is True


def test_outcome__outstanding_debt__with_mixed_outstanding_debts():
    model = under_test.Outcome(
        effective_date=None,
        debt_outcomes=[
            under_test.DebtOutcome(debt_name='jazz 1', debt_total=0.00),
            under_test.DebtOutcome(debt_name='jazz 2', debt_total=1000.00)
        ]
    )
    assert model.outstanding_debt() is True

