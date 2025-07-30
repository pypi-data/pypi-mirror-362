"""
Jama Unit Test Manager - Orchestrates UT creation workflow.

This module handles the complete workflow for creating unit tests in Jama:
1. Validate SmlPrep-UT-1 exists
2. Find/create module folder
3. Find/create unit tests
4. Create verification relationships
"""

import logging
from typing import Dict, List, Optional

from sw_ut_report.jama_common import JamaUTManager, JamaConnectionError, validate_environment, clean_log_message


def dry_run_unit_tests_creation(module_name: str, test_results: List[Dict]) -> bool:
    """
    Dry-run function to analyze what would be done without making changes to Jama.
    Logs errors and continues processing. Raises exception at the end if any errors occurred.

    Args:
        module_name: Name of the module (for folder creation)
        test_results: List of parsed test results from TXT/XML files

    Returns:
        bool: True if analysis succeeded

    Raises:
        JamaConnectionError: If any errors occurred during validation
    """
    logging.info(f"=== DRY-RUN: Analyzing Jama UT Creation for Module: {module_name} ===")

    # Validate environment first
    if not validate_environment():
        print("ISSUE: Jama environment not properly configured")
        return False

    try:
        # Initialize Jama manager
        jama_manager = JamaUTManager()
        print("Jama connection: OK")

        # Step 1: Check SmlPrep-SET-359 exists
        print("\n=== STEP 1: Checking SmlPrep-SET-359 ===")
        try:
            smlprep_set_359 = jama_manager.validate_smlprep_set_359_exists()
            print(f"FOUND: SmlPrep-SET-359 exists - {smlprep_set_359['fields']['name']}")
            print(f"   ID: {smlprep_set_359['id']}")
        except JamaConnectionError as e:
            print(f"ISSUE: {e}")
            return False

        # Step 2: Check module folder status
        print(f"\n=== STEP 2: Checking Module Folder: {module_name} ===")
        module_folder = _dry_run_check_module_folder(jama_manager, module_name, smlprep_set_359)

        # Rest of the analysis remains the same...
        print(f"\n=== STEP 3: Analyzing Test Cases ===")
        planned_actions = []
        total_scenarios = 0

        for test_result in test_results:
            if test_result.get('type') == 'txt':
                scenarios = test_result.get('content', [])

                for scenario in scenarios:
                    total_scenarios += 1

                    # Extract test name and covers
                    if 'test_case' in scenario:
                        test_name = scenario['test_case']
                        covers_list = scenario.get('covers_list', [])
                        source_info = f"Structured TXT: {test_result.get('filename', 'Unknown')}"
                    elif 'raw_lines' in scenario:
                        # Unstructured scenario - extract test name from first meaningful line
                        filename = test_result.get('filename', 'Unknown')

                        # Try to extract test name from first meaningful line
                        test_name = filename.replace('.txt', '') if filename.endswith('.txt') else filename  # fallback

                        if scenario.get('raw_lines'):
                            for line in scenario['raw_lines']:
                                clean_line = line.strip()
                                # Skip empty lines and covers lines
                                if clean_line and not clean_line.lower().startswith('covers:'):
                                    # Remove status indicators and use as test name
                                    import re
                                    clean_test_name = re.sub(r'\s+[🟢🔴⚪]\s+(PASS|FAIL|SKIP)\s*$', '', clean_line).strip()
                                    if clean_test_name:
                                        test_name = clean_test_name
                                        break

                        covers_list = scenario.get('covers_list', [])
                        source_info = f"Unstructured TXT: {filename}"
                    else:
                        print(f"SKIP: Unknown scenario format in {test_result.get('filename')}")
                        continue

                    # Analyze this test case
                    action = _dry_run_analyze_test_case(jama_manager, test_name, covers_list, source_info, module_folder)
                    planned_actions.append(action)

            elif test_result.get('type') == 'xml':
                total_scenarios += 1
                content = test_result.get('content', {})
                filename = test_result.get('filename', 'Unknown')
                test_name = content.get('name', filename.replace('.xml', '') if filename.endswith('.xml') else filename)
                covers_list = []
                source_info = f"XML: {filename}"

                # Analyze XML test case
                action = _dry_run_analyze_test_case(jama_manager, test_name, covers_list, source_info, module_folder)
                planned_actions.append(action)

        # Step 4: Summary Report
        print(f"\n=== DRY-RUN SUMMARY ===")
        print(f"📊 Module: {module_name}")
        print(f"📊 Total scenarios analyzed: {total_scenarios}")

        # Count actions
        new_tests = sum(1 for a in planned_actions if a['action'] == 'CREATE_TEST')
        existing_tests = sum(1 for a in planned_actions if a['action'] == 'EXISTS_TEST')
        new_relationships = sum(len(a['new_relationships']) for a in planned_actions)
        existing_relationships = sum(len(a['existing_relationships']) for a in planned_actions)

        print(f"📊 Unit tests to CREATE: {new_tests}")
        print(f"📊 Unit tests that EXIST: {existing_tests}")
        print(f"📊 Relationships to CREATE: {new_relationships}")
        print(f"📊 Relationships that EXIST: {existing_relationships}")
        print(f"📊 Status changes to 'Accepted': {total_scenarios}")  # All tests will have status changed

        # Detailed action report
        print(f"\n=== DETAILED ACTIONS ===")
        for i, action in enumerate(planned_actions, 1):
            print(f"\n{i}. {action['test_name']}")
            if action.get('original_test_name') != action['test_name']:
                print(f"   Original: {action['original_test_name']}")
            print(f"   Source: {action['source_info']}")

            if action['action'] == 'CREATE_TEST':
                print(f"   ACTION: Create new unit test")
            else:
                print(f"   EXISTS: Unit test already exists (ID: {action.get('existing_id', 'Unknown')})")

            if action['covers_list']:
                print(f"   Covers: {', '.join(action['covers_list'])}")

                if action['new_relationships']:
                    print(f"   Will create {len(action['new_relationships'])} new relationships:")
                    for rel in action['new_relationships']:
                        print(f"      -> {rel}")

                if action['existing_relationships']:
                    print(f"   {len(action['existing_relationships'])} relationships already exist:")
                    for rel in action['existing_relationships']:
                        print(f"      -> {rel}")

                if action['invalid_requirements']:
                    print(f"   {len(action['invalid_requirements'])} invalid requirements:")
                    for req in action['invalid_requirements']:
                        print(f"      -> {req} (NOT FOUND IN JAMA)")
            else:
                print(f"   No covers requirements")

            # Status change information
            print(f"   STATUS: Will change workflow status to 'Accepted'")

        # Check for issues
        has_issues = any(a['invalid_requirements'] for a in planned_actions)

        if has_issues:
            print(f"\nISSUES DETECTED:")
            print(f"   Some requirement IDs in 'covers' fields don't exist in Jama")
            print(f"   These will cause errors during execution")

            # Collect all invalid requirements for error reporting
            all_invalid_reqs = []
            for action in planned_actions:
                all_invalid_reqs.extend(action['invalid_requirements'])

            error_msg = f"Invalid requirements found during dry-run: {', '.join(set(all_invalid_reqs))}"
            logging.error(error_msg)

            from .jama_common import JamaConnectionError
            raise JamaConnectionError(error_msg)
        else:
            print(f"\nNO ISSUES DETECTED")
            print(f"   All requirements exist and operations look good!")
            return True

    except JamaConnectionError:
        raise
    except Exception as e:
        print(f"Unexpected error in dry-run analysis: {e}")
        return False


def _dry_run_check_module_folder(jama_manager: JamaUTManager, module_name: str, parent_item: Dict) -> Optional[Dict]:
    """Check if module folder exists without creating it under SmlPrep-SET-359."""
    try:
        parent_id = parent_item['id']

        print(f"DEBUG: Using SmlPrep-SET-359 ID {parent_id} for module folder search")

        # Try both methods: children API and location search
        children = jama_manager.get_children_items(parent_id)

        if not children:
            print("DEBUG: Children API returned 0, trying location search...")
            children = jama_manager.get_children_items_by_location(parent_id)

        print(f"DEBUG: Found {len(children)} children under SmlPrep-SET-359 (ID: {parent_id})")

        # Debug: Show all children
        for i, child in enumerate(children):
            child_name = child.get('fields', {}).get('name', 'NO_NAME')
            child_type = child.get('itemType', 'NO_TYPE')
            child_id = child.get('id', 'NO_ID')
            print(f"   {i+1}. {child_name} (Type: {child_type}, ID: {child_id})")

        # Look for existing module folder in direct children
        for child in children:
            child_name = child.get('fields', {}).get('name')
            child_type = child.get('itemType')

            print(f"Comparing: '{child_name}' == '{module_name}' AND {child_type} == 32")

            if (child_name == module_name and child_type == 32):  # FOLDER type
                print(f"FOUND: Module folder '{module_name}' already exists")
                print(f"   ID: {child['id']}")
                return child

        print(f"WILL CREATE: Module folder '{module_name}' under SmlPrep-SET-359")
        return {'id': 'NEW_FOLDER', 'fields': {'name': module_name}}  # Mock for analysis

    except Exception as e:
        print(f"Error checking module folder: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return None


def _dry_run_analyze_test_case(jama_manager: JamaUTManager, test_name: str, covers_list: List[str],
                              source_info: str, module_folder: Optional[Dict]) -> Dict:
    """Analyze a single test case for dry-run without making changes."""

    # Normalize test name for comparison
    normalized_test_name = jama_manager.normalize_test_name(test_name)

    action = {
        'test_name': normalized_test_name,  # Use normalized name
        'original_test_name': test_name,    # Keep original for reference
        'source_info': source_info,
        'covers_list': covers_list,
        'action': 'CREATE_TEST',
        'existing_id': None,
        'new_relationships': [],
        'existing_relationships': [],
        'invalid_requirements': []
    }

    # Check if unit test already exists
    if module_folder and module_folder.get('id') != 'NEW_FOLDER':
        try:
            module_folder_id = module_folder['id']

            # Get existing unit tests in this module folder
            children = jama_manager.get_children_items(module_folder_id)

            if not children:
                children = jama_manager.get_children_items_by_location(module_folder_id)

            # Look for existing unit test with same normalized name
            for child in children:
                if child.get('itemType') == 167:  # UNIT_TEST type
                    existing_name = child.get('fields', {}).get('name', '').strip()
                    normalized_existing = jama_manager.normalize_test_name(existing_name)

                    print(f"DRY-RUN: Comparing '{normalized_existing}' == '{normalized_test_name}'")

                    if normalized_existing == normalized_test_name:
                        action['action'] = 'EXISTS_TEST'
                        action['existing_id'] = child['id']
                        print(f"DRY-RUN: Found existing test '{existing_name}' (ID: {child['id']})")
                        break
        except Exception as e:
            print(f"Error checking existing tests: {e}")

    # Analyze covers relationships
    if covers_list:
        for requirement_id in covers_list:
            try:
                # Check if requirement exists in Jama
                req_item = jama_manager.get_item_by_document_key(requirement_id)
                if req_item:
                    # For dry-run, assume relationship will be created (we'd need to check existing relationships in real scenario)
                    action['new_relationships'].append(requirement_id)
                else:
                    action['invalid_requirements'].append(requirement_id)
            except JamaConnectionError:
                action['invalid_requirements'].append(requirement_id)

    return action


def create_unit_tests_in_jama(module_name: str, test_results: List[Dict]) -> bool:
    """
    Main function to create unit tests in Jama following the 4-step workflow.
    Logs errors and continues processing. Raises exception at the end if any errors occurred.

    Args:
        module_name: Name of the module (for folder creation)
        test_results: List of parsed test results from TXT/XML files

    Returns:
        bool: True if all operations succeeded

    Raises:
        JamaConnectionError: If any critical step fails or relationship creation errors occur
    """
    logging.info(f"=== Starting Jama UT Creation for Module: {module_name} ===")

    # Validate environment first
    if not validate_environment():
        raise JamaConnectionError("Jama environment not properly configured")

    try:
        # Initialize Jama manager
        jama_manager = JamaUTManager()
        logging.info("Jama UT Manager initialized successfully")

        # Step 1: Validate SmlPrep-SET-359 exists
        logging.info("=== Step 1: Validating SmlPrep-SET-359 ===")
        smlprep_set_359 = jama_manager.validate_smlprep_set_359_exists()

        # Step 2: Find or create module folder
        logging.info(f"=== Step 2: Finding/Creating Module Folder: {module_name} ===")
        module_folder = jama_manager.find_or_create_module_folder(module_name, smlprep_set_359)

        # Step 3 & 4: Process each test result
        logging.info("=== Step 3 & 4: Processing Test Cases ===")
        processed_count = 0
        total_scenarios = 0
        relationship_errors = []  # Track relationship creation failures
        status_change_errors = []  # Track status change failures

        for test_result in test_results:
            if test_result.get('type') == 'txt':
                # Handle TXT files with scenarios
                scenarios = test_result.get('content', [])

                for scenario in scenarios:
                    total_scenarios += 1

                    # Extract test name and covers
                    if 'test_case' in scenario:
                        # Structured scenario
                        test_name = scenario['test_case']
                        covers_list = scenario.get('covers_list', [])
                        test_content = scenario  # Pass the full scenario for description
                    elif 'raw_lines' in scenario:
                        # Unstructured scenario - extract test name from first meaningful line
                        filename = test_result.get('filename', 'Unknown')

                        # Try to extract test name from first meaningful line
                        test_name = filename.replace('.txt', '') if filename.endswith('.txt') else filename  # fallback

                        if scenario.get('raw_lines'):
                            for line in scenario['raw_lines']:
                                clean_line = line.strip()
                                # Skip empty lines and covers lines
                                if clean_line and not clean_line.lower().startswith('covers:'):
                                    # Remove status indicators and use as test name
                                    import re
                                    clean_test_name = re.sub(r'\s+[🟢🔴⚪]\s+(PASS|FAIL|SKIP)\s*$', '', clean_line).strip()
                                    if clean_test_name:
                                        test_name = clean_test_name
                                        break

                        covers_list = scenario.get('covers_list', [])
                        test_content = scenario  # Pass the raw content for description
                    else:
                        logging.warning(f"Skipping scenario with unknown format: {scenario}")
                        continue

                    # Step 3: Create unit test
                    logging.info(f"Creating UT: {clean_log_message(test_name)}")
                    unit_test = jama_manager.find_or_create_unit_test(test_name, module_folder, covers_list, test_content)

                    # Step 4: Create verification relationships
                    if covers_list:
                        logging.info(f"Creating relationships for {len(covers_list)} requirements")
                        try:
                            jama_manager.create_verification_relationships(unit_test, covers_list)
                            logging.info(f"Successfully created all relationships for {clean_log_message(test_name)}")
                        except JamaConnectionError as e:
                            logging.error(f"Failed to create relationships for {clean_log_message(test_name)}: {e}")
                            # Track the relationship error for summary reporting
                            relationship_errors.append({
                                'test_name': clean_log_message(test_name),
                                'covers_list': covers_list,
                                'error': str(e)
                            })
                            # Continue processing other tests - the error is already logged
                    else:
                        logging.info("No covers requirements found - no relationships to create")

                    # Step 5: Change workflow status to Accepted
                    try:
                        logging.info(f"Changing workflow status to 'Accepted' for {clean_log_message(test_name)}")
                        jama_manager.change_item_status_to_accepted(unit_test['id'])
                        logging.info(f"Successfully changed workflow status to 'Accepted' for {clean_log_message(test_name)}")
                    except JamaConnectionError as e:
                        logging.error(f"Failed to change workflow status for {clean_log_message(test_name)}: {e}")
                        # Track the status change error for summary reporting
                        status_change_errors.append({
                            'test_name': clean_log_message(test_name),
                            'test_id': unit_test['id'],
                            'error': str(e)
                        })
                        # Continue processing other tests - the error is already logged

                    processed_count += 1

            elif test_result.get('type') == 'xml':
                # Handle XML files - create one UT per XML file
                total_scenarios += 1
                content = test_result.get('content', {})
                filename = test_result.get('filename', 'Unknown')

                # Use XML suite name or filename as test name
                test_name = content.get('name', filename.replace('.xml', '') if filename.endswith('.xml') else filename)

                # XML files typically don't have covers - empty list
                covers_list = []

                # Create minimal test content for XML
                test_content = {
                    'xml_content': content,
                    'source_type': 'xml'
                }

                # Step 3: Create unit test
                logging.info(f"Creating UT from XML: {clean_log_message(test_name)}")
                unit_test = jama_manager.find_or_create_unit_test(test_name, module_folder, covers_list, test_content)

                # Step 4: No relationships for XML (no covers)
                logging.info("XML file - no covers requirements found")

                # Step 5: Change workflow status to Accepted for XML tests
                try:
                    logging.info(f"Changing workflow status to 'Accepted' for XML test {clean_log_message(test_name)}")
                    jama_manager.change_item_status_to_accepted(unit_test['id'])
                    logging.info(f"Successfully changed workflow status to 'Accepted' for XML test {clean_log_message(test_name)}")
                except JamaConnectionError as e:
                    logging.error(f"Failed to change workflow status for XML test {clean_log_message(test_name)}: {e}")
                    # Track the status change error for summary reporting
                    status_change_errors.append({
                        'test_name': clean_log_message(test_name),
                        'test_id': unit_test['id'],
                        'error': str(e)
                    })
                    # Continue processing other tests - the error is already logged

                processed_count += 1

            else:
                logging.warning(f"Skipping unknown test result type: {test_result.get('type')}")

        # Report final summary
        logging.info("=== UT Creation Summary ===")
        logging.info(f"Module: {module_name}")
        logging.info(f"Total scenarios processed: {total_scenarios}")
        logging.info(f"Successfully created/updated: {processed_count}")

        # Report relationship creation errors
        if relationship_errors:
            logging.error(f"Relationship creation failures: {len(relationship_errors)}")
            logging.error("Failed relationships details:")
            for error_info in relationship_errors:
                test_name = error_info['test_name']
                covers_count = len(error_info['covers_list'])
                error_msg = error_info['error']
                logging.error(f"  - {test_name}: Failed to create {covers_count} relationships")
                logging.error(f"    Error: {error_msg}")
        else:
            logging.info("All relationship operations completed successfully")

        # Report status change errors
        if status_change_errors:
            logging.error(f"Workflow status change failures: {len(status_change_errors)}")
            logging.error("Failed status changes details:")
            for error_info in status_change_errors:
                test_name = error_info['test_name']
                test_id = error_info['test_id']
                error_msg = error_info['error']
                logging.error(f"  - {test_name} (ID: {test_id}): Failed to change status to 'Accepted'")
                logging.error(f"    Error: {error_msg}")
        else:
            logging.info("All workflow status changes completed successfully")

        if processed_count > 0:
            total_errors = len(relationship_errors) + len(status_change_errors)
            if total_errors > 0:
                logging.warning(f"Processed {processed_count} unit tests but {total_errors} operations had failures")
                # Raise error to indicate partial failure
                failed_operations = []
                if relationship_errors:
                    failed_tests = [err['test_name'] for err in relationship_errors]
                    failed_operations.append(f"relationship creation failed for: {', '.join(failed_tests)}")
                if status_change_errors:
                    failed_tests = [err['test_name'] for err in status_change_errors]
                    failed_operations.append(f"status change failed for: {', '.join(failed_tests)}")
                raise JamaConnectionError(f"Unit tests processed but {'; '.join(failed_operations)}")
            else:
                logging.info(f"Successfully processed {processed_count} unit tests for module {module_name}")
                return True
        else:
            logging.warning("No unit tests were processed")
            return False

    except JamaConnectionError:
        # Re-raise Jama connection errors (these are expected and should stop execution)
        raise
    except Exception as e:
        logging.error(f"Unexpected error in UT creation workflow: {e}")
        raise JamaConnectionError(f"UT creation failed: {e}")


def extract_test_names_and_covers(test_results: List[Dict]) -> List[Dict]:
    """
    Extract test names and covers information from parsed test results.

    This function is useful for validation and preview purposes.

    Args:
        test_results: List of parsed test results

    Returns:
        List[Dict]: List of extracted test information
    """
    extracted_tests = []

    for test_result in test_results:
        if test_result.get('type') == 'txt':
            scenarios = test_result.get('content', [])

            for scenario in scenarios:
                if 'test_case' in scenario:
                    # Structured scenario
                    extracted_tests.append({
                        'test_name': scenario['test_case'],
                        'covers_list': scenario.get('covers_list', []),
                        'source_file': test_result.get('filename', 'Unknown'),
                        'type': 'structured_txt'
                    })
                elif 'raw_lines' in scenario:
                    # Unstructured scenario
                    filename = test_result.get('filename', 'Unknown')
                    test_name = filename.replace('.txt', '') if filename.endswith('.txt') else filename
                    extracted_tests.append({
                        'test_name': test_name,
                        'covers_list': scenario.get('covers_list', []),
                        'source_file': filename,
                        'type': 'unstructured_txt'
                    })

        elif test_result.get('type') == 'xml':
            content = test_result.get('content', {})
            filename = test_result.get('filename', 'Unknown')
            test_name = content.get('name', filename.replace('.xml', '') if filename.endswith('.xml') else filename)

            extracted_tests.append({
                'test_name': test_name,
                'covers_list': [],  # XML files don't have covers
                'source_file': filename,
                'type': 'xml'
            })

    return extracted_tests


def validate_jama_environment_for_ut_creation() -> bool:
    """
    Validate that the Jama environment is properly configured for UT creation.

    Returns:
        bool: True if environment is valid, False otherwise
    """
    try:
        # Check environment variables
        if not validate_environment():
            return False

        # Try to initialize manager and validate SmlPrep-UT-1
        jama_manager = JamaUTManager()
        jama_manager.validate_smlprep_ut_1_exists()

        logging.info("Jama environment validation successful")
        return True

    except JamaConnectionError as e:
        logging.error(f"Jama environment validation failed: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error during environment validation: {e}")
        return False