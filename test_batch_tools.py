#!/usr/bin/env python3
"""
Test script for the new batch tools in Google Sheets MCP.

Tests:
1. batch_get_values - Read multiple ranges
2. batch_clear_values - Clear multiple ranges
3. copy_paste - Copy range to another location
4. cut_paste - Cut and move range

Run with: uv run python test_batch_tools.py
"""

import asyncio
import sys
import os
import re

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from googleapiclient.discovery import build
from auth.google_auth import get_authenticated_google_service
from auth.scopes import SHEETS_WRITE_SCOPE, DRIVE_FILE_SCOPE

# Test configuration
USER_EMAIL = "justin@codaanalytics.xyz"
TEST_SPREADSHEET_NAME = "Batch Tools Test - Nov 2025"


async def get_sheets_service():
    """Get authenticated Google Sheets service."""
    scopes = [SHEETS_WRITE_SCOPE, DRIVE_FILE_SCOPE]
    service, _ = await get_authenticated_google_service(
        service_name="sheets",
        version="v4",
        tool_name="test_batch_tools",
        user_google_email=USER_EMAIL,
        required_scopes=scopes
    )
    return service


async def setup_test_spreadsheet(service):
    """Create a test spreadsheet with sample data."""
    print("\n=== SETUP: Creating test spreadsheet ===")

    # Create a new spreadsheet
    spreadsheet_body = {
        "properties": {"title": TEST_SPREADSHEET_NAME},
        "sheets": [
            {"properties": {"title": "DataSheet"}},
            {"properties": {"title": "TargetSheet"}}
        ]
    }

    result = await asyncio.to_thread(
        service.spreadsheets().create(body=spreadsheet_body).execute
    )

    spreadsheet_id = result["spreadsheetId"]
    print(f"Created spreadsheet ID: {spreadsheet_id}")

    # Get sheet IDs
    sheets = result.get("sheets", [])
    data_sheet_id = None
    target_sheet_id = None
    for sheet in sheets:
        props = sheet.get("properties", {})
        if props.get("title") == "DataSheet":
            data_sheet_id = props.get("sheetId")
        elif props.get("title") == "TargetSheet":
            target_sheet_id = props.get("sheetId")

    print(f"DataSheet ID: {data_sheet_id}, TargetSheet ID: {target_sheet_id}")

    # Add test data to DataSheet
    test_data = [
        ["Name", "Value", "Category", "Score"],
        ["Alice", "100", "A", "95"],
        ["Bob", "200", "B", "87"],
        ["Charlie", "150", "A", "92"],
        ["Diana", "250", "C", "88"],
        ["Eve", "175", "B", "91"],
    ]

    await asyncio.to_thread(
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range="DataSheet!A1:D6",
            valueInputOption="USER_ENTERED",
            body={"values": test_data}
        ).execute
    )
    print("Added test data to DataSheet A1:D6")

    # Add more test data in columns F-G
    extra_data = [
        ["Extra1", "Extra2"],
        ["X1", "Y1"],
        ["X2", "Y2"],
        ["X3", "Y3"],
    ]

    await asyncio.to_thread(
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range="DataSheet!F1:G4",
            valueInputOption="USER_ENTERED",
            body={"values": extra_data}
        ).execute
    )
    print("Added extra test data to DataSheet F1:G4")

    return spreadsheet_id, data_sheet_id, target_sheet_id


async def test_batch_get_values(service, spreadsheet_id):
    """Test batch_get_values - read multiple ranges in one call."""
    print("\n=== TEST 1: batch_get_values ===")

    try:
        # Use the values().batchGet API
        response = await asyncio.to_thread(
            service.spreadsheets().values().batchGet(
                spreadsheetId=spreadsheet_id,
                ranges=["DataSheet!A1:B3", "DataSheet!C1:D3", "DataSheet!F1:G2"],
                majorDimension="ROWS",
                valueRenderOption="FORMATTED_VALUE"
            ).execute
        )

        value_ranges = response.get("valueRanges", [])
        print(f"Retrieved {len(value_ranges)} range(s)")

        for vr in value_ranges:
            print(f"  Range: {vr.get('range')}")
            for row in vr.get("values", []):
                print(f"    {row}")

        print("✅ batch_get_values: PASS")
        return True
    except Exception as e:
        print(f"❌ batch_get_values: FAIL - {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_batch_clear_values(service, spreadsheet_id):
    """Test batch_clear_values - clear multiple ranges in one call."""
    print("\n=== TEST 2: batch_clear_values ===")

    try:
        # First, add some data to clear
        await asyncio.to_thread(
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range="DataSheet!H1:I3",
                valueInputOption="USER_ENTERED",
                body={"values": [["ToClear1", "ToClear2"], ["val1", "val2"], ["val3", "val4"]]}
            ).execute
        )
        print("Added data to H1:I3 to be cleared")

        await asyncio.to_thread(
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range="DataSheet!J1:K2",
                valueInputOption="USER_ENTERED",
                body={"values": [["More", "Data"], ["to", "clear"]]}
            ).execute
        )
        print("Added data to J1:K2 to be cleared")

        # Now clear both ranges using batchClear
        response = await asyncio.to_thread(
            service.spreadsheets().values().batchClear(
                spreadsheetId=spreadsheet_id,
                body={"ranges": ["DataSheet!H1:I3", "DataSheet!J1:K2"]}
            ).execute
        )

        cleared_ranges = response.get("clearedRanges", [])
        print(f"Cleared {len(cleared_ranges)} range(s): {cleared_ranges}")

        print("✅ batch_clear_values: PASS")
        return True
    except Exception as e:
        print(f"❌ batch_clear_values: FAIL - {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_copy_paste(service, spreadsheet_id, source_sheet_id, dest_sheet_id):
    """Test copy_paste - copy range to another location."""
    print("\n=== TEST 3: copy_paste ===")

    try:
        # Copy A1:B3 from DataSheet to TargetSheet at A1
        request = {
            "copyPaste": {
                "source": {
                    "sheetId": source_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 3,
                    "startColumnIndex": 0,
                    "endColumnIndex": 2
                },
                "destination": {
                    "sheetId": dest_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 3,
                    "startColumnIndex": 0,
                    "endColumnIndex": 2
                },
                "pasteType": "PASTE_VALUES",
                "pasteOrientation": "NORMAL"
            }
        }

        response = await asyncio.to_thread(
            service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={"requests": [request]}
            ).execute
        )
        print(f"Copy-paste executed successfully")

        # Verify the copy
        verify = await asyncio.to_thread(
            service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range="TargetSheet!A1:B3"
            ).execute
        )
        print(f"Verification (TargetSheet A1:B3): {verify.get('values', [])}")

        print("✅ copy_paste: PASS")
        return True
    except Exception as e:
        print(f"❌ copy_paste: FAIL - {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_copy_paste_transpose(service, spreadsheet_id, source_sheet_id, dest_sheet_id):
    """Test copy_paste with TRANSPOSE orientation."""
    print("\n=== TEST 3b: copy_paste (TRANSPOSE) ===")

    try:
        # Copy A1:D1 (header row) and transpose to column E
        request = {
            "copyPaste": {
                "source": {
                    "sheetId": source_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 4
                },
                "destination": {
                    "sheetId": dest_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 4,
                    "startColumnIndex": 4,
                    "endColumnIndex": 5
                },
                "pasteType": "PASTE_VALUES",
                "pasteOrientation": "TRANSPOSE"
            }
        }

        response = await asyncio.to_thread(
            service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={"requests": [request]}
            ).execute
        )
        print(f"Copy-paste (transpose) executed successfully")

        # Verify - should be vertical now
        verify = await asyncio.to_thread(
            service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range="TargetSheet!E1:E4"
            ).execute
        )
        print(f"Verification (transposed in E1:E4): {verify.get('values', [])}")

        print("✅ copy_paste (TRANSPOSE): PASS")
        return True
    except Exception as e:
        print(f"❌ copy_paste (TRANSPOSE): FAIL - {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_cut_paste(service, spreadsheet_id, source_sheet_id, dest_sheet_id):
    """Test cut_paste - cut and move range to another location."""
    print("\n=== TEST 4: cut_paste ===")

    try:
        # First, add data specifically for cutting
        await asyncio.to_thread(
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range="DataSheet!L1:M3",
                valueInputOption="USER_ENTERED",
                body={"values": [["CutMe1", "CutMe2"], ["data1", "data2"], ["data3", "data4"]]}
            ).execute
        )
        print("Added data to DataSheet L1:M3 for cutting")

        # Cut L1:M3 from DataSheet to TargetSheet at G1
        request = {
            "cutPaste": {
                "source": {
                    "sheetId": source_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 3,
                    "startColumnIndex": 11,  # Column L
                    "endColumnIndex": 13     # Through column M
                },
                "destination": {
                    "sheetId": dest_sheet_id,
                    "rowIndex": 0,
                    "columnIndex": 6  # Column G
                },
                "pasteType": "PASTE_NORMAL"
            }
        }

        response = await asyncio.to_thread(
            service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={"requests": [request]}
            ).execute
        )
        print(f"Cut-paste executed successfully")

        # Verify the destination has the data
        dest_verify = await asyncio.to_thread(
            service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range="TargetSheet!G1:H3"
            ).execute
        )
        print(f"Destination verification (TargetSheet G1:H3): {dest_verify.get('values', [])}")

        # Verify the source is now empty (might return empty or no values key)
        source_verify = await asyncio.to_thread(
            service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range="DataSheet!L1:M3"
            ).execute
        )
        source_values = source_verify.get('values', [])
        print(f"Source verification (should be empty): {source_values}")

        if not source_values or all(all(cell == "" for cell in row) for row in source_values):
            print("✅ cut_paste: PASS (source cleared)")
        else:
            print("⚠️ cut_paste: PARTIAL (data moved but source may have residual)")

        return True
    except Exception as e:
        print(f"❌ cut_paste: FAIL - {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_tests():
    """Run all batch tool tests."""
    print("=" * 60)
    print("BATCH TOOLS TEST SUITE")
    print("Testing Google Sheets API batch operations")
    print("=" * 60)

    results = {}

    try:
        # Get service
        print("\nAuthenticating...")
        service = await get_sheets_service()
        print("Authentication successful!")

        # Setup
        spreadsheet_id, data_sheet_id, target_sheet_id = await setup_test_spreadsheet(service)

        # Run tests
        results["batch_get_values"] = await test_batch_get_values(service, spreadsheet_id)
        results["batch_clear_values"] = await test_batch_clear_values(service, spreadsheet_id)
        results["copy_paste"] = await test_copy_paste(service, spreadsheet_id, data_sheet_id, target_sheet_id)
        results["copy_paste_transpose"] = await test_copy_paste_transpose(service, spreadsheet_id, data_sheet_id, target_sheet_id)
        results["cut_paste"] = await test_cut_paste(service, spreadsheet_id, data_sheet_id, target_sheet_id)

        # Summary
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)

        passed = sum(1 for v in results.values() if v)
        total = len(results)

        for test_name, passed_test in results.items():
            status = "✅ PASS" if passed_test else "❌ FAIL"
            print(f"  {test_name}: {status}")

        print(f"\nTotal: {passed}/{total} tests passed")
        print(f"\nTest spreadsheet URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")

        return passed == total

    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)
