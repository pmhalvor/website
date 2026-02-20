from config import Env


def check_wedding_invite(args: dict, env: Env):
    """
    Check if the query parameters match the expected values for the wedding invite.

    Expected query parameters:
        - who
        - when
        - where
        - activity

    Returns True if all parameters match, False otherwise.
    """

    expected_who = env.wedding_invite_who
    expected_when = env.wedding_invite_when
    expected_where = env.wedding_invite_where
    expected_activity = env.wedding_invite_activity

    print(
        f"Expected: who={expected_who}, "
        f"when={expected_when}, "
        f"where={expected_where}, "
        f"activity={expected_activity}"
    )
    print(
        f"Received: who={args.get('who')}, "
        f"when={args.get('when')}, "
        f"where={args.get('where')}, "
        f"activity={args.get('activity')}"
    )

    return (
        args.get("who") == expected_who and 
        args.get("when") == expected_when and 
        args.get("where") == expected_where and 
        args.get("activity") == expected_activity
    )