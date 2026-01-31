"""
Example usage of the Statistics Iceland API data fetcher.
"""

from data_fetcher import StatisticsIcelandAPI


def main():
    # Initialize the API client
    api = StatisticsIcelandAPI(language="is")
    
    print("=" * 60)
    print("Hagstofa Íslands - API Dæmi")
    print("=" * 60)
    print()
    
    # Example 1: Get available tables
    print("1. Sæki lista yfir tiltækar töflur...")
    tables = api.get_tables()
    if tables:
        print(f"   Fjöldi efnisflokka/taflna: {len(tables)}")
        # Show first few items
        for i, table in enumerate(tables[:5]):
            table_type = "Flokkur" if table.get('type') == 'l' else "Tafla"
            print(f"   - {table_type}: {table.get('text', 'N/A')}")
        if len(tables) > 5:
            print(f"   ... og {len(tables) - 5} fleiri")
    print()
    
    # Example 2: Search for specific tables
    print("2. Leita að töflum með leitarorðinu 'mannfjöldi'...")
    # Note: This may take some time as it searches through categories
    # Commented out to keep example quick
    # results = api.search_tables("mannfjöldi")
    # print(f"   Fjöldi niðurstaðna: {len(results)}")
    print("   (Slökkt á í þessu dæmi til að spara tíma)")
    print()
    
    # Example 3: Get metadata for a specific table
    print("3. Sæki metadata fyrir dæmi töflu...")
    # Using a common table path - this may need to be adjusted based on actual availability
    table_id = "Mannfjoldi/Yfirlit/mannfjoldi_yfirlit.px"
    metadata = api.get_table_metadata(table_id)
    if metadata:
        print(f"   Titill: {metadata.get('title', 'N/A')}")
        print(f"   Uppfært: {metadata.get('updated', 'N/A')}")
        if 'variables' in metadata:
            print(f"   Fjöldi breyta: {len(metadata['variables'])}")
    else:
        print("   Ekki tókst að sækja metadata (taflan er hugsanlega ekki til)")
    print()
    
    print("=" * 60)
    print("Dæmi lokið!")
    print("=" * 60)
    print()
    print("Til að keyra vefforritið:")
    print("  python app.py")
    print()
    print("Opnaðu síðan vafra á: http://localhost:5000")
    print()


if __name__ == "__main__":
    main()
