import asyncio
import pprint

from codesphere import CodesphereSDK


async def main():
    try:
        async with CodesphereSDK() as sdk:
            team_to_delete = await sdk.teams.get(team_id="<id>")
            print("\n--- Details of the team to be deleted ---")
            pprint.pprint(team_to_delete.model_dump())
            await team_to_delete.delete()
            print(f"Team with ID {team_to_delete.id} was successfully deleted.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
