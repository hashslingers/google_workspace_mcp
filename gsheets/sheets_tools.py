"""
Google Sheets MCP Tools

This module provides MCP tools for interacting with Google Sheets API.
"""

import logging
import asyncio
from typing import List, Optional


from auth.service_decorator import require_google_service
from core.server import server
from core.utils import handle_http_errors
from core.comments import create_comment_tools

# Configure module logger
logger = logging.getLogger(__name__)


@server.tool()
@handle_http_errors("list_spreadsheets", is_read_only=True)
@require_google_service("drive", "drive_read")
async def list_spreadsheets(
    service,
    user_google_email: str,
    max_results: int = 25,
) -> str:
    """
    Lists spreadsheets from Google Drive that the user has access to.

    Args:
        user_google_email (str): The user's Google email address. Required.
        max_results (int): Maximum number of spreadsheets to return. Defaults to 25.

    Returns:
        str: A formatted list of spreadsheet files (name, ID, modified time).
    """
    logger.info(f"[list_spreadsheets] Invoked. Email: '{user_google_email}'")

    files_response = await asyncio.to_thread(
        service.files()
        .list(
            q="mimeType='application/vnd.google-apps.spreadsheet'",
            pageSize=max_results,
            fields="files(id,name,modifiedTime,webViewLink)",
            orderBy="modifiedTime desc",
        )
        .execute
    )

    files = files_response.get("files", [])
    if not files:
        return f"No spreadsheets found for {user_google_email}."

    spreadsheets_list = [
        f"- \"{file['name']}\" (ID: {file['id']}) | Modified: {file.get('modifiedTime', 'Unknown')} | Link: {file.get('webViewLink', 'No link')}"
        for file in files
    ]

    text_output = (
        f"Successfully listed {len(files)} spreadsheets for {user_google_email}:\n"
        + "\n".join(spreadsheets_list)
    )

    logger.info(f"Successfully listed {len(files)} spreadsheets for {user_google_email}.")
    return text_output


@server.tool()
@handle_http_errors("get_spreadsheet_info", is_read_only=True)
@require_google_service("sheets", "sheets_read")
async def get_spreadsheet_info(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    include_data_preview: bool = True,
) -> str:
    """
    Gets detailed information about a spreadsheet including sheets, merged cells, named ranges, and data structure.

    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet to get info for. Required.
        include_data_preview (bool): Whether to include a preview of data from each sheet. Defaults to True.

    Returns:
        str: Comprehensive spreadsheet information including structure details.
    """
    logger.info(f"[get_spreadsheet_info] Invoked. Email: '{user_google_email}', Spreadsheet ID: {spreadsheet_id}")

    # Get spreadsheet with all metadata including sheets and named ranges
    spreadsheet = await asyncio.to_thread(
        service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            includeGridData=False,  # We'll fetch grid data separately for specific ranges
            fields="properties,sheets,namedRanges"
        ).execute
    )

    title = spreadsheet.get("properties", {}).get("title", "Unknown")
    sheets = spreadsheet.get("sheets", [])
    named_ranges = spreadsheet.get("namedRanges", [])

    # Format named ranges
    named_ranges_info = []
    if named_ranges:
        named_ranges_info.append("\nNamed Ranges:")
        for nr in named_ranges:
            name = nr.get("name", "Unknown")
            range_data = nr.get("range", {})
            sheet_id = range_data.get("sheetId")
            
            # Find sheet name from sheet ID
            sheet_name = "Unknown"
            for sheet in sheets:
                if sheet.get("properties", {}).get("sheetId") == sheet_id:
                    sheet_name = sheet.get("properties", {}).get("title")
                    break
            
            start_row = range_data.get("startRowIndex", 0)
            end_row = range_data.get("endRowIndex", 0)
            start_col = range_data.get("startColumnIndex", 0)
            end_col = range_data.get("endColumnIndex", 0)
            
            # Convert to A1 notation (approximation)
            col_letter = chr(65 + start_col) if start_col < 26 else f"{chr(65 + start_col // 26 - 1)}{chr(65 + start_col % 26)}"
            col_letter_end = chr(65 + end_col - 1) if end_col <= 26 else f"{chr(65 + (end_col - 1) // 26 - 1)}{chr(65 + (end_col - 1) % 26)}"
            
            named_ranges_info.append(
                f"  - {name}: {sheet_name}!{col_letter}{start_row + 1}:{col_letter_end}{end_row}"
            )

    # Process each sheet
    sheets_info = []
    for sheet in sheets:
        sheet_props = sheet.get("properties", {})
        sheet_name = sheet_props.get("title", "Unknown")
        sheet_id = sheet_props.get("sheetId", "Unknown")
        grid_props = sheet_props.get("gridProperties", {})
        rows = grid_props.get("rowCount", 0)
        cols = grid_props.get("columnCount", 0)

        sheet_info = [f"\n{'='*50}"]
        sheet_info.append(f"Sheet: \"{sheet_name}\" (ID: {sheet_id})")
        sheet_info.append(f"Size: {rows} rows × {cols} columns")

        # Get merged cells
        merges = sheet.get("merges", [])
        if merges:
            sheet_info.append(f"\nMerged Cells ({len(merges)} regions):")
            for merge in merges[:10]:  # Limit to first 10 for readability
                start_row = merge.get("startRowIndex", 0)
                end_row = merge.get("endRowIndex", 0)
                start_col = merge.get("startColumnIndex", 0)
                end_col = merge.get("endColumnIndex", 0)
                
                # Convert to A1 notation
                col_letter = chr(65 + start_col) if start_col < 26 else f"{chr(65 + start_col // 26 - 1)}{chr(65 + start_col % 26)}"
                col_letter_end = chr(65 + end_col - 1) if end_col <= 26 else f"{chr(65 + (end_col - 1) // 26 - 1)}{chr(65 + (end_col - 1) % 26)}"
                
                sheet_info.append(
                    f"  - {col_letter}{start_row + 1}:{col_letter_end}{end_row} "
                    f"({end_row - start_row} rows × {end_col - start_col} cols)"
                )
            if len(merges) > 10:
                sheet_info.append(f"  ... and {len(merges) - 10} more merged regions")

        # Get data preview if requested
        if include_data_preview and rows > 0 and cols > 0:
            try:
                # Intelligently determine range to check - first 20 rows, up to column Z
                preview_range = f"{sheet_name}!A1:Z{min(20, rows)}"
                
                result = await asyncio.to_thread(
                    service.spreadsheets()
                    .values()
                    .get(spreadsheetId=spreadsheet_id, range=preview_range)
                    .execute
                )
                
                values = result.get("values", [])
                if values:
                    # Detect actual data boundaries
                    non_empty_rows = 0
                    max_col_with_data = 0
                    first_row_with_data = -1
                    
                    for i, row in enumerate(values):
                        if any(cell.strip() for cell in row if cell):
                            non_empty_rows += 1
                            if first_row_with_data == -1:
                                first_row_with_data = i
                            max_col_with_data = max(max_col_with_data, 
                                                   max((j for j, cell in enumerate(row) if cell and cell.strip()), default=0))
                    
                    if non_empty_rows > 0:
                        sheet_info.append(f"\nData Preview:")
                        sheet_info.append(f"  - First row with data: Row {first_row_with_data + 1}")
                        sheet_info.append(f"  - Non-empty rows in preview: {non_empty_rows}")
                        sheet_info.append(f"  - Columns with data: A to {chr(65 + max_col_with_data)}")
                        
                        # Show first few rows
                        sheet_info.append(f"  - First 3 rows of data:")
                        shown_rows = 0
                        for i, row in enumerate(values):
                            if any(cell.strip() for cell in row if cell):
                                # Truncate long cells and limit columns shown
                                display_row = [cell[:30] + "..." if len(cell) > 30 else cell 
                                             for cell in row[:min(len(row), 5)]]
                                sheet_info.append(f"    Row {i + 1}: {display_row}")
                                shown_rows += 1
                                if shown_rows >= 3:
                                    break
                    else:
                        sheet_info.append(f"\nNo data found in preview range")
                        
            except Exception as e:
                sheet_info.append(f"\nCould not fetch data preview: {str(e)}")

        sheets_info.extend(sheet_info)

    # Build final output
    text_output = f"Spreadsheet: \"{title}\" (ID: {spreadsheet_id})\n"
    text_output += f"Total Sheets: {len(sheets)}"
    
    if named_ranges_info:
        text_output += "\n" + "\n".join(named_ranges_info)
    
    text_output += "\n" + "\n".join(sheets_info)

    logger.info(f"Successfully retrieved detailed info for spreadsheet {spreadsheet_id}")
    return text_output


def _convert_indices_to_a1(start_row, end_row, start_col, end_col):
    """Helper function to convert row/col indices to A1 notation."""
    def col_to_letter(col):
        if col < 26:
            return chr(65 + col)
        else:
            return chr(65 + col // 26 - 1) + chr(65 + col % 26)
    
    start_col_letter = col_to_letter(start_col)
    end_col_letter = col_to_letter(end_col - 1)  # end_col is exclusive
    
    return f"{start_col_letter}{start_row + 1}:{end_col_letter}{end_row}"


def _parse_a1_to_indices(a1_range):
    """Helper function to parse A1 notation to row/col indices."""
    import re
    
    # Handle sheet name if present
    if '!' in a1_range:
        sheet_name, a1_range = a1_range.split('!', 1)
    else:
        sheet_name = None
    
    # Parse the range
    match = re.match(r'([A-Z]+)(\d+):([A-Z]+)(\d+)', a1_range)
    if not match:
        # Try single cell
        match = re.match(r'([A-Z]+)(\d+)', a1_range)
        if match:
            col = match.group(1)
            row = int(match.group(2))
            col_idx = sum((ord(c) - 65) * (26 ** i) for i, c in enumerate(reversed(col)))
            return sheet_name, row - 1, row, col_idx, col_idx + 1
        return sheet_name, None, None, None, None
    
    start_col, start_row, end_col, end_row = match.groups()
    
    # Convert column letters to indices
    start_col_idx = sum((ord(c) - 65) * (26 ** i) for i, c in enumerate(reversed(start_col)))
    end_col_idx = sum((ord(c) - 65) * (26 ** i) for i, c in enumerate(reversed(end_col))) + 1  # exclusive
    
    return sheet_name, int(start_row) - 1, int(end_row), start_col_idx, end_col_idx


@server.tool()
@handle_http_errors("read_sheet_values", is_read_only=True)
@require_google_service("sheets", "sheets_read")
async def read_sheet_values(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    range_name: str = "A1:Z1000",
    handle_merged_cells: bool = True,
) -> str:
    """
    Reads values from a specific range in a Google Sheet with intelligent handling of merged cells.

    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
        range_name (str): The range to read (e.g., "Sheet1!A1:D10", "A1:D10"). Defaults to "A1:Z1000".
        handle_merged_cells (bool): Whether to detect and annotate merged cells. Defaults to True.

    Returns:
        str: The formatted values from the specified range with merged cell annotations.
    """
    logger.info(f"[read_sheet_values] Invoked. Email: '{user_google_email}', Spreadsheet: {spreadsheet_id}, Range: {range_name}")

    # Get the values
    result = await asyncio.to_thread(
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute
    )

    values = result.get("values", [])
    if not values:
        return f"No data found in range '{range_name}' for {user_google_email}."

    # Parse the range to determine sheet and boundaries
    sheet_name, start_row_idx, end_row_idx, start_col_idx, end_col_idx = _parse_a1_to_indices(range_name)
    
    # Get merged cells information if requested
    merged_regions = []
    if handle_merged_cells:
        try:
            # Get full spreadsheet data to access merge information
            spreadsheet = await asyncio.to_thread(
                service.spreadsheets().get(
                    spreadsheetId=spreadsheet_id,
                    fields="sheets.properties,sheets.merges"
                ).execute
            )
            
            # Find the right sheet
            target_sheet = None
            for sheet in spreadsheet.get("sheets", []):
                sheet_props = sheet.get("properties", {})
                if sheet_name is None or sheet_props.get("title") == sheet_name:
                    target_sheet = sheet
                    if sheet_name is None:
                        sheet_name = sheet_props.get("title")
                    break
            
            if target_sheet:
                merges = target_sheet.get("merges", [])
                # Filter merges that overlap with our range
                for merge in merges:
                    m_start_row = merge.get("startRowIndex", 0)
                    m_end_row = merge.get("endRowIndex", 0)
                    m_start_col = merge.get("startColumnIndex", 0)
                    m_end_col = merge.get("endColumnIndex", 0)
                    
                    # Check if merge overlaps with our range
                    if (start_row_idx is not None and 
                        m_start_row < end_row_idx and m_end_row > start_row_idx and
                        m_start_col < end_col_idx and m_end_col > start_col_idx):
                        merged_regions.append({
                            "start_row": m_start_row,
                            "end_row": m_end_row,
                            "start_col": m_start_col,
                            "end_col": m_end_col,
                            "a1": _convert_indices_to_a1(m_start_row, m_end_row, m_start_col, m_end_col)
                        })
        except Exception as e:
            logger.warning(f"Could not fetch merge information: {e}")

    # Format the output
    formatted_rows = []
    
    # Add merge information header if merges exist
    if merged_regions:
        formatted_rows.append("MERGED CELLS DETECTED:")
        for merge in merged_regions[:10]:  # Limit display
            formatted_rows.append(f"  - {merge['a1']} ({merge['end_row'] - merge['start_row']} rows × {merge['end_col'] - merge['start_col']} cols)")
        if len(merged_regions) > 10:
            formatted_rows.append(f"  ... and {len(merged_regions) - 10} more merged regions")
        formatted_rows.append("\nDATA VALUES:")
    
    # Determine if we have a header row (first row with multiple non-empty cells)
    has_header = False
    if values and len(values[0]) > 1:
        non_empty_in_first = sum(1 for cell in values[0] if cell and cell.strip())
        if non_empty_in_first >= 2:
            has_header = True
            formatted_rows.append(f"Header Row: {values[0]}")
            formatted_rows.append("-" * 50)
    
    # Format data rows
    start_idx = 1 if has_header else 0
    for i, row in enumerate(values[start_idx:], start_idx + 1):
        # Check if this row is affected by merges
        merge_annotations = []
        if merged_regions and start_row_idx is not None:
            actual_row_idx = start_row_idx + i - 1
            for merge in merged_regions:
                if merge["start_row"] <= actual_row_idx < merge["end_row"]:
                    merge_annotations.append(f"[MERGED: {merge['a1']}]")
        
        # Pad row with empty strings to show structure
        padded_row = row + [""] * max(0, len(values[0]) - len(row)) if values else row
        
        row_str = f"Row {i:3d}: {padded_row}"
        if merge_annotations:
            row_str += " " + " ".join(merge_annotations)
        
        formatted_rows.append(row_str)
        
        # Limit output for readability
        if len(formatted_rows) > 60:
            formatted_rows.append(f"... and {len(values) - i} more rows")
            break

    text_output = (
        f"Successfully read {len(values)} rows from range '{range_name}' in spreadsheet {spreadsheet_id} for {user_google_email}.\n"
        + "\n".join(formatted_rows)
    )

    logger.info(f"Successfully read {len(values)} rows with {len(merged_regions)} merged regions for {user_google_email}.")
    return text_output


@server.tool()
@handle_http_errors("modify_sheet_values")
@require_google_service("sheets", "sheets_write")
async def modify_sheet_values(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    range_name: str,
    values: Optional[List[List[str]]] = None,
    value_input_option: str = "USER_ENTERED",
    clear_values: bool = False,
) -> str:
    """
    Modifies values in a specific range of a Google Sheet - can write, update, or clear values.

    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
        range_name (str): The range to modify (e.g., "Sheet1!A1:D10", "A1:D10"). Required.
        values (Optional[List[List[str]]]): 2D array of values to write/update. Required unless clear_values=True.
        value_input_option (str): How to interpret input values ("RAW" or "USER_ENTERED"). Defaults to "USER_ENTERED".
        clear_values (bool): If True, clears the range instead of writing values. Defaults to False.

    Returns:
        str: Confirmation message of the successful modification operation.
    """
    operation = "clear" if clear_values else "write"
    logger.info(f"[modify_sheet_values] Invoked. Operation: {operation}, Email: '{user_google_email}', Spreadsheet: {spreadsheet_id}, Range: {range_name}")

    if not clear_values and not values:
        raise Exception("Either 'values' must be provided or 'clear_values' must be True.")

    if clear_values:
        result = await asyncio.to_thread(
            service.spreadsheets()
            .values()
            .clear(spreadsheetId=spreadsheet_id, range=range_name)
            .execute
        )

        cleared_range = result.get("clearedRange", range_name)
        text_output = f"Successfully cleared range '{cleared_range}' in spreadsheet {spreadsheet_id} for {user_google_email}."
        logger.info(f"Successfully cleared range '{cleared_range}' for {user_google_email}.")
    else:
        body = {"values": values}

        result = await asyncio.to_thread(
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute
        )

        updated_cells = result.get("updatedCells", 0)
        updated_rows = result.get("updatedRows", 0)
        updated_columns = result.get("updatedColumns", 0)

        text_output = (
            f"Successfully updated range '{range_name}' in spreadsheet {spreadsheet_id} for {user_google_email}. "
            f"Updated: {updated_cells} cells, {updated_rows} rows, {updated_columns} columns."
        )
        logger.info(f"Successfully updated {updated_cells} cells for {user_google_email}.")

    return text_output


@server.tool()
@handle_http_errors("create_spreadsheet")
@require_google_service("sheets", "sheets_write")
async def create_spreadsheet(
    service,
    user_google_email: str,
    title: str,
    sheet_names: Optional[List[str]] = None,
) -> str:
    """
    Creates a new Google Spreadsheet.

    Args:
        user_google_email (str): The user's Google email address. Required.
        title (str): The title of the new spreadsheet. Required.
        sheet_names (Optional[List[str]]): List of sheet names to create. If not provided, creates one sheet with default name.

    Returns:
        str: Information about the newly created spreadsheet including ID and URL.
    """
    logger.info(f"[create_spreadsheet] Invoked. Email: '{user_google_email}', Title: {title}")

    spreadsheet_body = {
        "properties": {
            "title": title
        }
    }

    if sheet_names:
        spreadsheet_body["sheets"] = [
            {"properties": {"title": sheet_name}} for sheet_name in sheet_names
        ]

    spreadsheet = await asyncio.to_thread(
        service.spreadsheets().create(body=spreadsheet_body).execute
    )

    spreadsheet_id = spreadsheet.get("spreadsheetId")
    spreadsheet_url = spreadsheet.get("spreadsheetUrl")

    text_output = (
        f"Successfully created spreadsheet '{title}' for {user_google_email}. "
        f"ID: {spreadsheet_id} | URL: {spreadsheet_url}"
    )

    logger.info(f"Successfully created spreadsheet for {user_google_email}. ID: {spreadsheet_id}")
    return text_output


@server.tool()
@handle_http_errors("create_sheet")
@require_google_service("sheets", "sheets_write")
async def create_sheet(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    sheet_name: str,
) -> str:
    """
    Creates a new sheet within an existing spreadsheet.

    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
        sheet_name (str): The name of the new sheet. Required.

    Returns:
        str: Confirmation message of the successful sheet creation.
    """
    logger.info(f"[create_sheet] Invoked. Email: '{user_google_email}', Spreadsheet: {spreadsheet_id}, Sheet: {sheet_name}")

    request_body = {
        "requests": [
            {
                "addSheet": {
                    "properties": {
                        "title": sheet_name
                    }
                }
            }
        ]
    }

    response = await asyncio.to_thread(
        service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        .execute
    )

    sheet_id = response["replies"][0]["addSheet"]["properties"]["sheetId"]

    text_output = (
        f"Successfully created sheet '{sheet_name}' (ID: {sheet_id}) in spreadsheet {spreadsheet_id} for {user_google_email}."
    )

    logger.info(f"Successfully created sheet for {user_google_email}. Sheet ID: {sheet_id}")
    return text_output


@server.tool()
@require_google_service("sheets", "sheets_write")
@handle_http_errors("format_cells")
async def format_cells(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    range_name: str,
    background_color: Optional[dict] = None,
    text_format: Optional[dict] = None,
    horizontal_alignment: Optional[str] = None,
    vertical_alignment: Optional[str] = None,
    borders: Optional[dict] = None,
    number_format: Optional[dict] = None,
) -> str:
    """
    Format cells in a spreadsheet with various styling options.
    
    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
        range_name (str): The A1 notation range to format (e.g., "Sheet1!A1:D10"). Required.
        background_color (dict): RGB color {"red": 0.0-1.0, "green": 0.0-1.0, "blue": 0.0-1.0}
        text_format (dict): Text formatting options:
            {
                "foregroundColor": {"red": 0.0-1.0, "green": 0.0-1.0, "blue": 0.0-1.0},
                "fontSize": 10,
                "bold": True/False,
                "italic": True/False,
                "strikethrough": True/False,
                "underline": True/False,
                "fontFamily": "Arial"
            }
        horizontal_alignment (str): "LEFT", "CENTER", "RIGHT"
        vertical_alignment (str): "TOP", "MIDDLE", "BOTTOM"
        borders (dict): Border configuration:
            {
                "top": {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}},
                "bottom": {...},
                "left": {...},
                "right": {...}
            }
        number_format (dict): Number format configuration:
            {
                "type": "NUMBER" | "CURRENCY" | "PERCENT" | "DATE" | "TIME" | "DATE_TIME" | "SCIENTIFIC",
                "pattern": "0.00" | "$#,##0.00" | "0%" | "yyyy-mm-dd" | etc.
            }
    
    Returns:
        str: Confirmation message with the number of cells formatted.
    """
    logger.info(f"[format_cells] Invoked. Email: '{user_google_email}', Spreadsheet: {spreadsheet_id}, Range: {range_name}")
    
    # Parse the range to get sheet name and grid range
    sheet_name, start_row_idx, end_row_idx, start_col_idx, end_col_idx = _parse_a1_to_indices(range_name)
    
    # Get sheet ID
    spreadsheet = await asyncio.to_thread(
        service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="sheets.properties"
        ).execute
    )
    
    sheet_id = None
    for sheet in spreadsheet.get("sheets", []):
        if sheet["properties"]["title"] == sheet_name:
            sheet_id = sheet["properties"]["sheetId"]
            break
    
    if sheet_id is None:
        raise Exception(f"Sheet '{sheet_name}' not found in spreadsheet")
    
    # Build the format request
    requests = []
    
    # Cell format object
    cell_format = {}
    
    if background_color:
        cell_format["backgroundColor"] = background_color
    
    if text_format:
        cell_format["textFormat"] = text_format
    
    if horizontal_alignment:
        cell_format["horizontalAlignment"] = horizontal_alignment
    
    if vertical_alignment:
        cell_format["verticalAlignment"] = vertical_alignment
    
    if borders:
        # Convert friendly border format to API format
        cell_format["borders"] = {}
        for side, border_config in borders.items():
            if side in ["top", "bottom", "left", "right"]:
                cell_format["borders"][side] = {
                    "style": border_config.get("style", "SOLID"),
                    "width": border_config.get("width", 1),
                    "color": border_config.get("color", {"red": 0, "green": 0, "blue": 0})
                }
    
    if number_format:
        cell_format["numberFormat"] = number_format
    
    # Create the format request
    if cell_format:
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": start_row_idx,
                    "endRowIndex": end_row_idx,
                    "startColumnIndex": start_col_idx,
                    "endColumnIndex": end_col_idx
                },
                "cell": {
                    "userEnteredFormat": cell_format
                },
                "fields": "userEnteredFormat"
            }
        })
    
    if not requests:
        return f"No formatting options provided for range '{range_name}'"
    
    # Execute the batch update
    body = {"requests": requests}
    response = await asyncio.to_thread(
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute
    )
    
    # Calculate cells formatted
    cells_formatted = (end_row_idx - start_row_idx) * (end_col_idx - start_col_idx)
    
    text_output = (
        f"Successfully formatted {cells_formatted} cells in range '{range_name}' "
        f"in spreadsheet {spreadsheet_id} for {user_google_email}."
    )
    
    # Add details about what was formatted
    format_details = []
    if background_color:
        format_details.append("background color")
    if text_format:
        format_details.append("text format")
    if horizontal_alignment or vertical_alignment:
        format_details.append("alignment")
    if borders:
        format_details.append("borders")
    if number_format:
        format_details.append("number format")
    
    if format_details:
        text_output += f" Applied: {', '.join(format_details)}."
    
    logger.info(f"Successfully formatted {cells_formatted} cells for {user_google_email}")
    return text_output


@server.tool()
@require_google_service("sheets", "sheets_write")
@handle_http_errors("merge_cells")
async def merge_cells(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    range_name: str,
    merge_type: str = "MERGE_ALL",
) -> str:
    """
    Merge cells in a spreadsheet range.
    
    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
        range_name (str): The A1 notation range to merge (e.g., "Sheet1!A1:C3"). Required.
        merge_type (str): Type of merge operation. Options:
            - "MERGE_ALL": Merge all cells in the range into one cell (default)
            - "MERGE_COLUMNS": Merge cells in each column individually
            - "MERGE_ROWS": Merge cells in each row individually
    
    Returns:
        str: Confirmation message with the merge operation details.
    """
    logger.info(f"[merge_cells] Invoked. Email: '{user_google_email}', Spreadsheet: {spreadsheet_id}, Range: {range_name}")
    
    # Parse the range to get sheet name and grid range
    sheet_name, start_row_idx, end_row_idx, start_col_idx, end_col_idx = _parse_a1_to_indices(range_name)
    
    # Get sheet ID
    spreadsheet = await asyncio.to_thread(
        service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="sheets.properties"
        ).execute
    )
    
    sheet_id = None
    for sheet in spreadsheet.get("sheets", []):
        if sheet["properties"]["title"] == sheet_name:
            sheet_id = sheet["properties"]["sheetId"]
            break
    
    if sheet_id is None:
        raise Exception(f"Sheet '{sheet_name}' not found in spreadsheet")
    
    # Create merge request
    request = {
        "mergeCells": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row_idx,
                "endRowIndex": end_row_idx,
                "startColumnIndex": start_col_idx,
                "endColumnIndex": end_col_idx
            },
            "mergeType": merge_type
        }
    }
    
    # Execute the batch update
    body = {"requests": [request]}
    response = await asyncio.to_thread(
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute
    )
    
    # Calculate merge details
    rows_merged = end_row_idx - start_row_idx
    cols_merged = end_col_idx - start_col_idx
    
    merge_description = {
        "MERGE_ALL": f"Merged all {rows_merged * cols_merged} cells into one",
        "MERGE_COLUMNS": f"Merged {rows_merged} rows in each of {cols_merged} columns",
        "MERGE_ROWS": f"Merged {cols_merged} columns in each of {rows_merged} rows"
    }
    
    text_output = (
        f"Successfully merged cells in range '{range_name}' in spreadsheet {spreadsheet_id} for {user_google_email}. "
        f"{merge_description.get(merge_type, 'Merge operation completed')}."
    )
    
    logger.info(f"Successfully merged cells for {user_google_email}")
    return text_output


@server.tool()
@require_google_service("sheets", "sheets_write")
@handle_http_errors("unmerge_cells")
async def unmerge_cells(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    range_name: str,
) -> str:
    """
    Unmerge all merged cells within a range.
    
    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
        range_name (str): The A1 notation range containing merged cells to unmerge (e.g., "Sheet1!A1:C3"). Required.
    
    Returns:
        str: Confirmation message with the number of cells unmerged.
    """
    logger.info(f"[unmerge_cells] Invoked. Email: '{user_google_email}', Spreadsheet: {spreadsheet_id}, Range: {range_name}")
    
    # Parse the range to get sheet name and grid range
    sheet_name, start_row_idx, end_row_idx, start_col_idx, end_col_idx = _parse_a1_to_indices(range_name)
    
    # Get sheet ID
    spreadsheet = await asyncio.to_thread(
        service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="sheets.properties"
        ).execute
    )
    
    sheet_id = None
    for sheet in spreadsheet.get("sheets", []):
        if sheet["properties"]["title"] == sheet_name:
            sheet_id = sheet["properties"]["sheetId"]
            break
    
    if sheet_id is None:
        raise Exception(f"Sheet '{sheet_name}' not found in spreadsheet")
    
    # Create unmerge request
    request = {
        "unmergeCells": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row_idx,
                "endRowIndex": end_row_idx,
                "startColumnIndex": start_col_idx,
                "endColumnIndex": end_col_idx
            }
        }
    }
    
    # Execute the batch update
    body = {"requests": [request]}
    response = await asyncio.to_thread(
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute
    )
    
    text_output = (
        f"Successfully unmerged all cells in range '{range_name}' in spreadsheet {spreadsheet_id} for {user_google_email}."
    )
    
    logger.info(f"Successfully unmerged cells for {user_google_email}")
    return text_output


@server.tool()
@require_google_service("sheets", "sheets_write")
@handle_http_errors("create_named_range")
async def create_named_range(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    name: str,
    range_name: str,
) -> str:
    """
    Create a named range in a spreadsheet.
    
    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
        name (str): The name for the named range (e.g., "SalesData"). Required.
        range_name (str): The A1 notation range to name (e.g., "Sheet1!A1:D10"). Required.
    
    Returns:
        str: Confirmation message with the named range details.
    """
    logger.info(f"[create_named_range] Invoked. Email: '{user_google_email}', Spreadsheet: {spreadsheet_id}, Name: {name}")
    
    # Parse the range to get sheet name and grid range
    sheet_name, start_row_idx, end_row_idx, start_col_idx, end_col_idx = _parse_a1_to_indices(range_name)
    
    # Get sheet ID
    spreadsheet = await asyncio.to_thread(
        service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="sheets.properties"
        ).execute
    )
    
    sheet_id = None
    for sheet in spreadsheet.get("sheets", []):
        if sheet["properties"]["title"] == sheet_name:
            sheet_id = sheet["properties"]["sheetId"]
            break
    
    if sheet_id is None:
        raise Exception(f"Sheet '{sheet_name}' not found in spreadsheet")
    
    # Create named range request
    request = {
        "addNamedRange": {
            "namedRange": {
                "name": name,
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": start_row_idx,
                    "endRowIndex": end_row_idx,
                    "startColumnIndex": start_col_idx,
                    "endColumnIndex": end_col_idx
                }
            }
        }
    }
    
    # Execute the batch update
    body = {"requests": [request]}
    response = await asyncio.to_thread(
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute
    )
    
    text_output = (
        f"Successfully created named range '{name}' for range '{range_name}' "
        f"in spreadsheet {spreadsheet_id} for {user_google_email}."
    )
    
    logger.info(f"Successfully created named range '{name}' for {user_google_email}")
    return text_output


@server.tool()
@require_google_service("sheets", "sheets_read")
@handle_http_errors("list_named_ranges")
async def list_named_ranges(
    service,
    user_google_email: str,
    spreadsheet_id: str,
) -> str:
    """
    List all named ranges in a spreadsheet.
    
    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
    
    Returns:
        str: List of named ranges with their details.
    """
    logger.info(f"[list_named_ranges] Invoked. Email: '{user_google_email}', Spreadsheet: {spreadsheet_id}")
    
    # Get spreadsheet with named ranges
    spreadsheet = await asyncio.to_thread(
        service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="properties.title,sheets.properties,namedRanges"
        ).execute
    )
    
    spreadsheet_title = spreadsheet.get("properties", {}).get("title", "Unknown")
    named_ranges = spreadsheet.get("namedRanges", [])
    sheets = spreadsheet.get("sheets", [])
    
    # Create sheet ID to name mapping
    sheet_id_to_name = {}
    for sheet in sheets:
        sheet_props = sheet.get("properties", {})
        sheet_id_to_name[sheet_props.get("sheetId")] = sheet_props.get("title", "Unknown")
    
    if not named_ranges:
        return f"No named ranges found in spreadsheet '{spreadsheet_title}' for {user_google_email}."
    
    # Format named ranges
    ranges_list = []
    for nr in named_ranges:
        name = nr.get("name", "Unknown")
        named_range_id = nr.get("namedRangeId", "Unknown")
        range_data = nr.get("range", {})
        sheet_id = range_data.get("sheetId")
        sheet_name = sheet_id_to_name.get(sheet_id, "Unknown")
        
        start_row = range_data.get("startRowIndex", 0)
        end_row = range_data.get("endRowIndex", 0)
        start_col = range_data.get("startColumnIndex", 0)
        end_col = range_data.get("endColumnIndex", 0)
        
        # Convert to A1 notation
        a1_range = _convert_indices_to_a1(start_row, end_row, start_col, end_col)
        full_range = f"{sheet_name}!{a1_range}"
        
        ranges_list.append(
            f"- '{name}' (ID: {named_range_id}): {full_range}"
        )
    
    text_output = (
        f"Found {len(named_ranges)} named ranges in spreadsheet '{spreadsheet_title}' for {user_google_email}:\n"
        + "\n".join(ranges_list)
    )
    
    logger.info(f"Successfully listed {len(named_ranges)} named ranges for {user_google_email}")
    return text_output


@server.tool()
@require_google_service("sheets", "sheets_write")
@handle_http_errors("delete_named_range")
async def delete_named_range(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    named_range_id: str,
) -> str:
    """
    Delete a named range from a spreadsheet.
    
    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
        named_range_id (str): The ID of the named range to delete. Required.
    
    Returns:
        str: Confirmation message.
    """
    logger.info(f"[delete_named_range] Invoked. Email: '{user_google_email}', Spreadsheet: {spreadsheet_id}, Named Range ID: {named_range_id}")
    
    # Create delete request
    request = {
        "deleteNamedRange": {
            "namedRangeId": named_range_id
        }
    }
    
    # Execute the batch update
    body = {"requests": [request]}
    response = await asyncio.to_thread(
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute
    )
    
    text_output = (
        f"Successfully deleted named range with ID '{named_range_id}' "
        f"from spreadsheet {spreadsheet_id} for {user_google_email}."
    )
    
    logger.info(f"Successfully deleted named range for {user_google_email}")
    return text_output


@server.tool()
@require_google_service("sheets", "sheets_write")
@handle_http_errors("add_data_validation")
async def add_data_validation(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    range_name: str,
    validation_type: str,
    validation_config: dict,
    input_message: Optional[str] = None,
    reject_invalid: bool = True,
    show_dropdown: bool = True,
) -> str:
    """
    Add data validation to a range of cells.
    
    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
        range_name (str): The A1 notation range to validate (e.g., "Sheet1!A1:A10"). Required.
        validation_type (str): Type of validation. Options:
            - "LIST": Dropdown list from values
            - "NUMBER": Number constraints (>, <, >=, <=, ==, !=, BETWEEN)
            - "DATE": Date constraints
            - "TEXT_LENGTH": Text length constraints
            - "CUSTOM": Custom formula validation
            - "CHECKBOX": Boolean checkbox
        validation_config (dict): Configuration specific to validation type:
            For LIST: {"values": ["Option1", "Option2", ...]} or {"range": "Sheet1!A1:A10"}
            For NUMBER/DATE: {"condition": "GREATER_THAN", "value": 10} or 
                            {"condition": "BETWEEN", "values": [10, 100]}
            For TEXT_LENGTH: {"condition": "LESS_THAN", "value": 100}
            For CUSTOM: {"formula": "=A1>0"}
            For CHECKBOX: {} (no config needed)
        input_message (str): Help text shown when cell is selected. Optional.
        reject_invalid (bool): Whether to reject invalid input. Default True.
        show_dropdown (bool): Whether to show dropdown arrow for LIST type. Default True.
    
    Returns:
        str: Confirmation message with validation details.
    """
    logger.info(f"[add_data_validation] Invoked. Email: '{user_google_email}', Type: {validation_type}")
    
    # Parse the range
    sheet_name, start_row_idx, end_row_idx, start_col_idx, end_col_idx = _parse_a1_to_indices(range_name)
    
    # Get sheet ID
    spreadsheet = await asyncio.to_thread(
        service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="sheets.properties"
        ).execute
    )
    
    sheet_id = None
    for sheet in spreadsheet.get("sheets", []):
        if sheet["properties"]["title"] == sheet_name:
            sheet_id = sheet["properties"]["sheetId"]
            break
    
    if sheet_id is None:
        raise Exception(f"Sheet '{sheet_name}' not found in spreadsheet")
    
    # Build validation rule based on type
    rule = {
        "inputMessage": input_message or "",
        "strict": reject_invalid,
        "showCustomUi": show_dropdown if validation_type == "LIST" else True
    }
    
    if validation_type == "LIST":
        if "values" in validation_config:
            rule["condition"] = {
                "type": "ONE_OF_LIST",
                "values": [{"userEnteredValue": str(v)} for v in validation_config["values"]]
            }
        elif "range" in validation_config:
            # Parse range for source
            source_range = validation_config["range"]
            
            # Ensure the range has absolute references
            if "!" not in source_range:
                source_range = f"{sheet_name}!{source_range}"
            
            # Add absolute reference markers if not present
            if not source_range.startswith("="):
                source_range = "=" + source_range
            
            rule["condition"] = {
                "type": "ONE_OF_RANGE",
                "values": [{
                    "userEnteredValue": source_range
                }]
            }
    
    elif validation_type == "NUMBER":
        condition = validation_config.get("condition", "GREATER_THAN")
        if condition == "BETWEEN":
            rule["condition"] = {
                "type": "NUMBER_BETWEEN",
                "values": [
                    {"userEnteredValue": str(validation_config["values"][0])},
                    {"userEnteredValue": str(validation_config["values"][1])}
                ]
            }
        elif condition == "NOT_BETWEEN":
            rule["condition"] = {
                "type": "NUMBER_NOT_BETWEEN",
                "values": [
                    {"userEnteredValue": str(validation_config["values"][0])},
                    {"userEnteredValue": str(validation_config["values"][1])}
                ]
            }
        else:
            type_map = {
                "GREATER_THAN": "NUMBER_GREATER",
                "GREATER_THAN_OR_EQUAL": "NUMBER_GREATER_THAN_EQ",
                "LESS_THAN": "NUMBER_LESS",
                "LESS_THAN_OR_EQUAL": "NUMBER_LESS_THAN_EQ",
                "EQUAL": "NUMBER_EQ",
                "NOT_EQUAL": "NUMBER_NOT_EQ"
            }
            rule["condition"] = {
                "type": type_map.get(condition, "NUMBER_GREATER"),
                "values": [{"userEnteredValue": str(validation_config["value"])}]
            }
    
    elif validation_type == "DATE":
        condition = validation_config.get("condition", "GREATER_THAN")
        if condition == "BETWEEN":
            rule["condition"] = {
                "type": "DATE_BETWEEN",
                "values": [
                    {"userEnteredValue": validation_config["values"][0]},
                    {"userEnteredValue": validation_config["values"][1]}
                ]
            }
        else:
            type_map = {
                "GREATER_THAN": "DATE_AFTER",
                "LESS_THAN": "DATE_BEFORE",
                "EQUAL": "DATE_EQ"
            }
            rule["condition"] = {
                "type": type_map.get(condition, "DATE_AFTER"),
                "values": [{"userEnteredValue": validation_config["value"]}]
            }
    
    elif validation_type == "TEXT_LENGTH":
        # Google Sheets doesn't have direct text length validation, use custom formula
        condition = validation_config.get("condition", "LESS_THAN")
        value = validation_config.get("value")
        
        # Convert the A1 range to get the first cell for formula reference
        first_cell = range_name.split(":")[-1] if ":" in range_name else range_name
        if "!" in first_cell:
            first_cell = first_cell.split("!")[-1]
        
        # Build formula based on condition
        if condition == "LESS_THAN":
            formula = f"=LEN({first_cell})<{value}"
        elif condition == "LESS_THAN_OR_EQUAL":
            formula = f"=LEN({first_cell})<={value}"
        elif condition == "GREATER_THAN":
            formula = f"=LEN({first_cell})>{value}"
        elif condition == "GREATER_THAN_OR_EQUAL":
            formula = f"=LEN({first_cell})>={value}"
        elif condition == "BETWEEN":
            min_val, max_val = validation_config["values"]
            formula = f"=AND(LEN({first_cell})>={min_val},LEN({first_cell})<={max_val})"
        else:
            formula = f"=LEN({first_cell})<{value}"
        
        rule["condition"] = {
            "type": "CUSTOM_FORMULA",
            "values": [{"userEnteredValue": formula}]
        }
    
    elif validation_type == "CUSTOM":
        rule["condition"] = {
            "type": "CUSTOM_FORMULA",
            "values": [{"userEnteredValue": validation_config["formula"]}]
        }
    
    elif validation_type == "CHECKBOX":
        rule["condition"] = {
            "type": "BOOLEAN"
        }
    
    # Create the request
    request = {
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row_idx,
                "endRowIndex": end_row_idx,
                "startColumnIndex": start_col_idx,
                "endColumnIndex": end_col_idx
            },
            "rule": rule
        }
    }
    
    # Execute the batch update
    body = {"requests": [request]}
    response = await asyncio.to_thread(
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute
    )
    
    cells_validated = (end_row_idx - start_row_idx) * (end_col_idx - start_col_idx)
    
    text_output = (
        f"Successfully added {validation_type} validation to {cells_validated} cells "
        f"in range '{range_name}' in spreadsheet {spreadsheet_id} for {user_google_email}."
    )
    
    logger.info(f"Successfully added data validation for {user_google_email}")
    return text_output


@server.tool()
@require_google_service("sheets", "sheets_write")
@handle_http_errors("clear_data_validation")
async def clear_data_validation(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    range_name: str,
) -> str:
    """
    Clear data validation from a range of cells.
    
    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
        range_name (str): The A1 notation range to clear validation from. Required.
    
    Returns:
        str: Confirmation message.
    """
    logger.info(f"[clear_data_validation] Invoked. Email: '{user_google_email}', Range: {range_name}")
    
    # Parse the range
    sheet_name, start_row_idx, end_row_idx, start_col_idx, end_col_idx = _parse_a1_to_indices(range_name)
    
    # Get sheet ID
    spreadsheet = await asyncio.to_thread(
        service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="sheets.properties"
        ).execute
    )
    
    sheet_id = None
    for sheet in spreadsheet.get("sheets", []):
        if sheet["properties"]["title"] == sheet_name:
            sheet_id = sheet["properties"]["sheetId"]
            break
    
    if sheet_id is None:
        raise Exception(f"Sheet '{sheet_name}' not found in spreadsheet")
    
    # Create the request to clear validation
    request = {
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row_idx,
                "endRowIndex": end_row_idx,
                "startColumnIndex": start_col_idx,
                "endColumnIndex": end_col_idx
            }
            # Omitting 'rule' clears the validation
        }
    }
    
    # Execute the batch update
    body = {"requests": [request]}
    response = await asyncio.to_thread(
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute
    )
    
    text_output = (
        f"Successfully cleared data validation from range '{range_name}' "
        f"in spreadsheet {spreadsheet_id} for {user_google_email}."
    )
    
    logger.info(f"Successfully cleared data validation for {user_google_email}")
    return text_output


@server.tool()
@require_google_service("sheets", "sheets_write")
@handle_http_errors("add_conditional_formatting")
async def add_conditional_formatting(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    range_name: str,
    rule_type: str,
    rule_config: dict,
    format_config: Optional[dict] = None,
) -> str:
    """
    Add conditional formatting to a range of cells.
    
    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
        range_name (str): The A1 notation range to format (e.g., "Sheet1!A1:D10"). Required.
        rule_type (str): Type of conditional formatting rule:
            - "SINGLE_COLOR": Format based on cell values
            - "COLOR_SCALE": Gradient between 2-3 colors based on values
            - "CUSTOM_FORMULA": Format based on custom formula
        rule_config (dict): Configuration for the rule:
            For SINGLE_COLOR: {
                "condition_type": "NUMBER_GREATER", "NUMBER_LESS", "NUMBER_BETWEEN", "TEXT_CONTAINS", etc.
                "values": [value1, value2] or [value] depending on condition
            }
            For COLOR_SCALE: {
                "min_type": "MIN", "NUMBER", "PERCENT", "PERCENTILE"
                "min_value": value (if type is not MIN)
                "mid_type": "MEDIAN", "NUMBER", "PERCENT", "PERCENTILE" (optional)
                "mid_value": value (if mid_type is specified)
                "max_type": "MAX", "NUMBER", "PERCENT", "PERCENTILE"
                "max_value": value (if type is not MAX)
                "min_color": {"red": 0.0-1.0, "green": 0.0-1.0, "blue": 0.0-1.0}
                "mid_color": {...} (if using 3-color gradient)
                "max_color": {...}
            }
            For DATA_BAR: {
                "min_type": "MIN", "NUMBER", "PERCENT", "PERCENTILE"
                "min_value": value (if type is not MIN)
                "max_type": "MAX", "NUMBER", "PERCENT", "PERCENTILE"
                "max_value": value (if type is not MAX)
                "color": {"red": 0.0-1.0, "green": 0.0-1.0, "blue": 0.0-1.0}
                "direction": "LEFT_TO_RIGHT" or "RIGHT_TO_LEFT"
            }
            For CUSTOM_FORMULA: {
                "formula": "=$A1>100" (use absolute column references)
            }
        format_config (dict): Format to apply when condition is met (for SINGLE_COLOR and CUSTOM_FORMULA):
            {
                "backgroundColor": {"red": 0.0-1.0, "green": 0.0-1.0, "blue": 0.0-1.0},
                "textFormat": {"bold": true, "foregroundColor": {...}, ...}
            }
    
    Returns:
        str: Confirmation message with the conditional formatting details.
    """
    logger.info(f"[add_conditional_formatting] Invoked. Type: {rule_type}")
    
    # Parse the range
    sheet_name, start_row_idx, end_row_idx, start_col_idx, end_col_idx = _parse_a1_to_indices(range_name)
    
    # Get sheet ID
    spreadsheet = await asyncio.to_thread(
        service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="sheets.properties"
        ).execute
    )
    
    sheet_id = None
    for sheet in spreadsheet.get("sheets", []):
        if sheet["properties"]["title"] == sheet_name:
            sheet_id = sheet["properties"]["sheetId"]
            break
    
    if sheet_id is None:
        raise Exception(f"Sheet '{sheet_name}' not found in spreadsheet")
    
    # Build the conditional format rule
    ranges = [{
        "sheetId": sheet_id,
        "startRowIndex": start_row_idx,
        "endRowIndex": end_row_idx,
        "startColumnIndex": start_col_idx,
        "endColumnIndex": end_col_idx
    }]
    
    if rule_type == "SINGLE_COLOR":
        condition_type = rule_config.get("condition_type", "NUMBER_GREATER")
        values = rule_config.get("values", [])
        
        condition = {"type": condition_type}
        if values:
            condition["values"] = [{"userEnteredValue": str(v)} for v in values]
        
        rule = {
            "ranges": ranges,
            "booleanRule": {
                "condition": condition,
                "format": format_config
            }
        }
    
    elif rule_type == "COLOR_SCALE":
        # Build gradient rule
        min_point = {
            "type": rule_config.get("min_type", "MIN"),
            "color": rule_config.get("min_color", {"red": 1, "green": 0, "blue": 0})
        }
        if "min_value" in rule_config:
            min_point["value"] = str(rule_config["min_value"])
        
        max_point = {
            "type": rule_config.get("max_type", "MAX"),
            "color": rule_config.get("max_color", {"red": 0, "green": 1, "blue": 0})
        }
        if "max_value" in rule_config:
            max_point["value"] = str(rule_config["max_value"])
        
        gradient_rule = {
            "minpoint": min_point,
            "maxpoint": max_point
        }
        
        # Add midpoint if specified
        if "mid_type" in rule_config:
            mid_point = {
                "type": rule_config["mid_type"],
                "color": rule_config.get("mid_color", {"red": 1, "green": 1, "blue": 0})
            }
            if "mid_value" in rule_config:
                mid_point["value"] = str(rule_config["mid_value"])
            gradient_rule["midpoint"] = mid_point
        
        rule = {
            "ranges": ranges,
            "gradientRule": gradient_rule
        }
    
    elif rule_type == "DATA_BAR":
        # Build data bar rule
        min_point = {
            "type": rule_config.get("min_type", "MIN")
        }
        if "min_value" in rule_config:
            min_point["value"] = str(rule_config["min_value"])
        
        max_point = {
            "type": rule_config.get("max_type", "MAX")
        }
        if "max_value" in rule_config:
            max_point["value"] = str(rule_config["max_value"])
        
        rule = {
            "ranges": ranges,
            "dataBarRule": {
                "minPoint": min_point,
                "maxPoint": max_point,
                "color": rule_config.get("color", {"red": 0.2, "green": 0.5, "blue": 1}),
                "direction": rule_config.get("direction", "LEFT_TO_RIGHT"),
                "showValue": rule_config.get("show_value", True)
            }
        }
    
    elif rule_type == "CUSTOM_FORMULA":
        rule = {
            "ranges": ranges,
            "booleanRule": {
                "condition": {
                    "type": "CUSTOM_FORMULA",
                    "values": [{"userEnteredValue": rule_config["formula"]}]
                },
                "format": format_config
            }
        }
    
    # Create the request
    request = {
        "addConditionalFormatRule": {
            "rule": rule,
            "index": 0  # Add at the beginning (highest priority)
        }
    }
    
    # Execute the batch update
    body = {"requests": [request]}
    response = await asyncio.to_thread(
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute
    )
    
    cells_formatted = (end_row_idx - start_row_idx) * (end_col_idx - start_col_idx)
    
    text_output = (
        f"Successfully added {rule_type} conditional formatting to {cells_formatted} cells "
        f"in range '{range_name}' in spreadsheet {spreadsheet_id} for {user_google_email}."
    )
    
    logger.info(f"Successfully added conditional formatting for {user_google_email}")
    return text_output


@server.tool()
@require_google_service("sheets", "sheets_write")
@handle_http_errors("clear_conditional_formatting")
async def clear_conditional_formatting(
    service,
    user_google_email: str,
    spreadsheet_id: str,
    sheet_name: Optional[str] = None,
) -> str:
    """
    Clear all conditional formatting rules from a sheet or entire spreadsheet.
    
    Args:
        user_google_email (str): The user's Google email address. Required.
        spreadsheet_id (str): The ID of the spreadsheet. Required.
        sheet_name (str): Name of specific sheet to clear. If None, clears all sheets. Optional.
    
    Returns:
        str: Confirmation message.
    """
    logger.info(f"[clear_conditional_formatting] Invoked. Sheet: {sheet_name or 'All'}")
    
    # Get spreadsheet with conditional format rules
    spreadsheet = await asyncio.to_thread(
        service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="sheets.properties,sheets.conditionalFormats"
        ).execute
    )
    
    requests = []
    rules_cleared = 0
    
    for sheet in spreadsheet.get("sheets", []):
        sheet_props = sheet.get("properties", {})
        current_sheet_name = sheet_props.get("title")
        sheet_id = sheet_props.get("sheetId")
        
        # Skip if we're targeting a specific sheet and this isn't it
        if sheet_name and current_sheet_name != sheet_name:
            continue
        
        # Get conditional formats for this sheet
        conditional_formats = sheet.get("conditionalFormats", [])
        
        # Create delete requests for each rule
        for i, rule in enumerate(conditional_formats):
            requests.append({
                "deleteConditionalFormatRule": {
                    "sheetId": sheet_id,
                    "index": 0  # Always delete index 0 as rules shift down
                }
            })
            rules_cleared += 1
    
    if not requests:
        return f"No conditional formatting rules found to clear for {user_google_email}."
    
    # Execute the batch update
    body = {"requests": requests}
    response = await asyncio.to_thread(
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute
    )
    
    scope = f"sheet '{sheet_name}'" if sheet_name else "all sheets"
    text_output = (
        f"Successfully cleared {rules_cleared} conditional formatting rules from {scope} "
        f"in spreadsheet {spreadsheet_id} for {user_google_email}."
    )
    
    logger.info(f"Successfully cleared conditional formatting for {user_google_email}")
    return text_output


# Create comment management tools for sheets
_comment_tools = create_comment_tools("spreadsheet", "spreadsheet_id")

# Extract and register the functions
read_sheet_comments = _comment_tools['read_comments']
create_sheet_comment = _comment_tools['create_comment']
reply_to_sheet_comment = _comment_tools['reply_to_comment']
resolve_sheet_comment = _comment_tools['resolve_comment']


