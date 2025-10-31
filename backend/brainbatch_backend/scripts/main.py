import user_management as um
import group_management as gm
from uuid import UUID
from db_connect import init_client


def main():
    init_client()

    #print(gm.create_group("Tester Group", "cbb50222-66fc-4cb4-a9bf-81388f44e36e"))
    #print(gm.send_message("a29791bb-cb47-4d13-a55a-d298283dae7e", "cbb50222-66fc-4cb4-a9bf-81388f44e36e", "general", "Testing chat messages"))
    print(gm.add_chat_area("a29791bb-cb47-4d13-a55a-d298283dae7e", "tester area"))
    print(gm.send_message("a29791bb-cb47-4d13-a55a-d298283dae7e", "cbb50222-66fc-4cb4-a9bf-81388f44e36e", "tester area", "Tesint new chat area"))


if __name__ == "__main__":
    main()
