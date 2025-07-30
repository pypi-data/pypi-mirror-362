#!/usr/bin/env python3
"""
Frontend tests using real experiment data.

These tests require real experiment data in experiment-data/phase2_june/
and will be skipped if the data is not available.
"""

from playwright.sync_api import expect


def test_adm_selection_updates_llm(page, real_data_test_server):
    """Test that selecting an ADM type updates the LLM dropdown."""
    page.goto(real_data_test_server)

    # Wait for table to load
    page.wait_for_selector(".comparison-table", timeout=10000)
    page.wait_for_function(
        "document.querySelectorAll('.table-adm-select').length > 0", timeout=10000
    )

    adm_select = page.locator(".table-adm-select").first
    llm_select = page.locator(".table-llm-select").first

    # Select an ADM type
    adm_select.select_option("pipeline_baseline")

    # Wait for LLM dropdown to update
    page.wait_for_timeout(500)

    # Check that LLM dropdown has options
    expect(llm_select).to_be_visible()
    llm_options = llm_select.locator("option").all()
    assert len(llm_options) > 0, "LLM dropdown should have options after ADM selection"


def test_kdma_sliders_interaction(page, real_data_test_server):
    """Test that KDMA sliders are interactive and snap to valid values."""
    page.goto(real_data_test_server)

    # Wait for table to load
    page.wait_for_selector(".comparison-table", timeout=10000)
    page.wait_for_function(
        "document.querySelectorAll('.table-adm-select').length > 0", timeout=10000
    )

    # Set ADM type to enable KDMA sliders
    adm_select = page.locator(".table-adm-select").first
    adm_select.select_option("pipeline_baseline")
    # Wait for UI to update after ADM selection
    page.wait_for_load_state("networkidle")

    # Find KDMA sliders in table
    sliders = page.locator(".table-kdma-value-slider").all()

    if sliders:
        slider = sliders[0]
        value_span = slider.locator("xpath=following-sibling::span[1]")

        # Get initial value
        initial_value = value_span.text_content()

        # Try to change slider value - it should snap to nearest valid value
        slider.evaluate("slider => slider.value = '0.7'")
        slider.dispatch_event("input")

        # Wait for value to update
        page.wait_for_timeout(500)

        new_value = value_span.text_content()
        # Value should change from initial (validation may snap it to valid value)
        assert new_value != initial_value or float(new_value) in [
            0.0,
            0.1,
            0.2,
            0.3,
            0.4,
            0.5,
            0.6,
            0.7,
            0.8,
            0.9,
            1.0,
        ], f"Slider value should be valid decimal, got {new_value}"


def test_scenario_selection_availability(page, real_data_test_server):
    """Test that scenario selection becomes available after parameter selection."""
    page.goto(real_data_test_server)

    # Wait for table to load
    page.wait_for_selector(".comparison-table", timeout=10000)
    page.wait_for_function(
        "document.querySelectorAll('.table-adm-select').length > 0", timeout=10000
    )

    # Make selections
    adm_select = page.locator(".table-adm-select").first
    adm_select.select_option("pipeline_baseline")

    # Wait a moment for updates
    page.wait_for_timeout(1000)

    # Check scenario dropdown in table
    scenario_select = page.locator(".table-scenario-select").first
    expect(scenario_select).to_be_visible()

    # It should either have options or be disabled with a message
    if scenario_select.is_enabled():
        scenario_options = scenario_select.locator("option").all()
        assert len(scenario_options) > 0, (
            "Enabled scenario dropdown should have options"
        )
    else:
        # If disabled, it should have a "no scenarios" message
        disabled_option = scenario_select.locator("option").first
        expect(disabled_option).to_contain_text("No scenarios available")


def test_dynamic_kdma_management(page, real_data_test_server):
    """Test dynamic KDMA addition, removal, and type selection."""
    page.goto(real_data_test_server)

    # Wait for table to load
    page.wait_for_selector(".comparison-table", timeout=10000)
    page.wait_for_function(
        "document.querySelectorAll('.table-adm-select').length > 0", timeout=10000
    )

    # Select ADM and LLM to enable KDMA functionality
    adm_select = page.locator(".table-adm-select").first
    adm_select.select_option("pipeline_baseline")
    page.wait_for_timeout(1000)

    # Check KDMA controls in table
    kdma_sliders = page.locator(".table-kdma-value-slider")
    initial_count = kdma_sliders.count()

    # Should have KDMA sliders available in the table
    assert initial_count > 0, "Should have KDMA sliders in table after ADM selection"

    # Check KDMA slider functionality
    if initial_count > 0:
        first_slider = kdma_sliders.first
        expect(first_slider).to_be_visible()

        # Test slider interaction
        first_slider.fill("0.7")
        page.wait_for_timeout(500)

        new_value = first_slider.input_value()
        assert new_value == "0.7", "KDMA slider should update value"


def test_kdma_selection_shows_results_regression(page, real_data_test_server):
    """Test that KDMA sliders work correctly in the table-based UI."""
    page.goto(real_data_test_server)

    # Wait for page to load
    page.wait_for_selector(".comparison-table", timeout=10000)
    page.wait_for_function(
        "document.querySelectorAll('.table-adm-select').length > 0", timeout=10000
    )

    # Test basic table-based KDMA functionality
    adm_select = page.locator(".table-adm-select").first

    # Select pipeline_baseline to enable KDMA sliders
    adm_select.select_option("pipeline_baseline")
    page.wait_for_timeout(1000)

    # Check for KDMA sliders in the table
    kdma_sliders = page.locator(".table-kdma-value-slider")
    slider_count = kdma_sliders.count()

    if slider_count > 0:
        print(f"Testing {slider_count} KDMA sliders")

        # Test that sliders are functional
        first_slider = kdma_sliders.first
        first_slider.fill("0.7")
        page.wait_for_timeout(500)

        # Verify slider works
        assert first_slider.input_value() == "0.7", "KDMA slider should be functional"

        # Verify table remains functional
        expect(page.locator(".comparison-table")).to_be_visible()
        print("✓ KDMA functionality test passed")
    else:
        print("No KDMA sliders found - test passes")


def test_real_data_scenario_availability(page, real_data_test_server):
    """Test that scenarios are available with real data."""
    page.goto(real_data_test_server)

    # Wait for table to load
    page.wait_for_selector(".comparison-table", timeout=10000)

    # For real data, we should have some data loaded
    # Even if no specific scenario elements, the table should be populated
    table_rows = page.locator(".comparison-table tbody tr")
    assert table_rows.count() > 0, "Should have data rows in the comparison table"


def test_real_data_comprehensive_loading(page, real_data_test_server):
    """Test comprehensive loading of real experiment data."""
    page.goto(real_data_test_server)

    # Wait for page to fully load
    page.wait_for_load_state("networkidle")

    # Check for no JavaScript errors
    js_errors = []
    page.on(
        "console",
        lambda msg: js_errors.append(msg.text) if msg.type == "error" else None,
    )

    # Wait for table to load
    page.wait_for_selector(".comparison-table", timeout=10000)

    # Give time for any async operations
    page.wait_for_timeout(2000)

    # Check that we have minimal expected elements
    expect(page.locator(".comparison-table")).to_be_visible()

    # Filter out known acceptable errors
    filtered_errors = [
        error
        for error in js_errors
        if not any(
            acceptable in error.lower()
            for acceptable in ["favicon", "manifest", "workbox", "service worker"]
        )
    ]

    assert len(filtered_errors) == 0, f"Found JavaScript errors: {filtered_errors}"


def test_kdma_combination_default_value_issue(page, real_data_test_server):
    """Test the KDMA combination issue where adding a second KDMA defaults to 0.5 instead of valid value."""
    page.goto(real_data_test_server)

    # Wait for table to load
    page.wait_for_selector(".comparison-table", timeout=10000)
    page.wait_for_function(
        "document.querySelectorAll('.table-adm-select').length > 0", timeout=10000
    )

    # Select pipeline_baseline ADM to enable KDMA functionality
    adm_select = page.locator(".table-adm-select").first
    adm_select.select_option("pipeline_baseline")
    # Wait for UI to update after ADM selection
    page.wait_for_load_state("networkidle")

    # Select June2025-AF-train scenario to get multi-KDMA support
    scenario_select = page.locator(".table-scenario-select").first

    # Check what scenarios are available
    scenario_options = scenario_select.locator("option").all()
    scenario_values = [
        opt.get_attribute("value")
        for opt in scenario_options
        if opt.get_attribute("value")
    ]
    print(f"Available scenarios: {scenario_values}")

    # Find a June2025-AF-train scenario (required for this test)
    june_scenarios = [s for s in scenario_values if "June2025-AF-train" in s]
    assert len(june_scenarios) > 0, (
        f"June2025-AF-train scenarios required for this test, but only found: {scenario_values}"
    )

    scenario_select.select_option(june_scenarios[0])
    # Wait for scenario selection to take effect
    page.wait_for_load_state("networkidle")

    # Check initial KDMA sliders - should have affiliation already
    kdma_sliders = page.locator(".table-kdma-value-slider")
    initial_count = kdma_sliders.count()

    # Should have at least one KDMA slider initially
    assert initial_count > 0, "Should have initial KDMA slider"

    # Look for "Add KDMA" button
    add_kdma_button = page.locator(".add-kdma-btn")

    # This test requires the ability to add a second KDMA
    assert add_kdma_button.count() > 0, (
        "Add KDMA button must be available for this test"
    )

    # Click Add KDMA button
    add_kdma_button.click()

    # Wait for new KDMA slider to be added by checking for count increase
    page.wait_for_function(
        f"document.querySelectorAll('.table-kdma-value-slider').length > {initial_count}",
        timeout=5000,
    )

    # Check that a new KDMA slider was added
    updated_kdma_sliders = page.locator(".table-kdma-value-slider")
    updated_count = updated_kdma_sliders.count()

    assert updated_count > initial_count, "Should have added a new KDMA slider"

    # Check the value of the new slider
    new_sliders = updated_kdma_sliders.all()
    if len(new_sliders) > 1:
        # Get the last slider (newly added)
        new_slider = new_sliders[-1]
        new_value = new_slider.input_value()

        # This is the bug: it defaults to 0.5 instead of a valid value
        # For pipeline_baseline with affiliation+merit, valid combinations are only 0.0 and 1.0
        # So 0.5 should not be the default - it should be 0.0 or 1.0
        valid_values = ["0.0", "1.0"]

        # This assertion should fail with current code, proving the bug exists
        # Accept both integer and decimal formats
        valid_values = ["0.0", "1.0", "0", "1"]
        assert new_value in valid_values, (
            f"New KDMA slider should default to valid value (0.0 or 1.0), but got {new_value}"
        )

    # Also check that the dropdowns don't go blank
    adm_select_value = adm_select.input_value()
    assert adm_select_value != "", "ADM select should not go blank after adding KDMA"

    scenario_select_value = scenario_select.input_value()
    assert scenario_select_value != "", (
        "Scenario select should not go blank after adding KDMA"
    )
    assert "June2025-AF-train" in scenario_select_value, (
        "Should still have June2025-AF-train scenario selected"
    )


def test_kdma_delete_button_enabled_after_adding_second_kdma(
    page, real_data_test_server
):
    """Test that KDMA delete buttons become enabled after adding a second KDMA when valid single-KDMA experiments exist."""
    page.goto(real_data_test_server)

    # Wait for table to load
    page.wait_for_selector(".comparison-table", timeout=10000)
    page.wait_for_function(
        "document.querySelectorAll('.table-adm-select').length > 0", timeout=10000
    )

    # Select pipeline_baseline ADM to enable KDMA functionality
    adm_select = page.locator(".table-adm-select").first
    adm_select.select_option("pipeline_baseline")
    page.wait_for_load_state("networkidle")

    # Select June2025-AF-train scenario to get multi-KDMA support
    scenario_select = page.locator(".table-scenario-select").first

    # Check what scenarios are available
    scenario_options = scenario_select.locator("option").all()
    scenario_values = [
        opt.get_attribute("value")
        for opt in scenario_options
        if opt.get_attribute("value")
    ]

    # Find a June2025-AF-train scenario (required for this test)
    june_scenarios = [s for s in scenario_values if "June2025-AF-train" in s]
    assert len(june_scenarios) > 0, (
        f"June2025-AF-train scenarios required for this test, but only found: {scenario_values}"
    )

    scenario_select.select_option(june_scenarios[0])
    page.wait_for_load_state("networkidle")

    # Check initial KDMA delete buttons - should be disabled with single KDMA
    initial_delete_buttons = page.locator(".table-kdma-remove-btn")
    initial_delete_count = initial_delete_buttons.count()

    # This test requires at least one initial delete button
    assert initial_delete_count > 0, (
        "Should have at least one delete button with initial KDMA"
    )

    initial_button = initial_delete_buttons.first
    initial_disabled = initial_button.is_disabled()
    print(f"Initial delete button disabled: {initial_disabled}")

    # With single KDMA, delete button should be disabled (can't remove all KDMAs)
    assert initial_disabled, "Delete button should be disabled with single KDMA"

    # Look for "Add KDMA" button
    add_kdma_button = page.locator(".add-kdma-btn")

    # This test requires the ability to add a second KDMA
    assert add_kdma_button.count() > 0, (
        "Add KDMA button must be available for this test"
    )

    # Click Add KDMA button to add second KDMA
    add_kdma_button.click()

    # Wait for new KDMA slider to be added
    page.wait_for_function(
        "document.querySelectorAll('.table-kdma-value-slider').length > 1", timeout=5000
    )

    # Now check delete buttons after adding second KDMA
    updated_delete_buttons = page.locator(".table-kdma-remove-btn")
    updated_delete_count = updated_delete_buttons.count()

    assert updated_delete_count > 1, "Should have delete buttons for multiple KDMAs"

    # Check delete button states for asymmetric KDMA deletion
    # With two KDMAs (affiliation + merit) for June2025-AF-train scenario:
    # - affiliation alone: experiments exist for this scenario ✅
    # - merit alone: experiments DON'T exist for this scenario (they exist for June2025-MF-train) ❌
    # Therefore: only merit KDMA should be deletable (leaving affiliation alone)
    all_delete_buttons = updated_delete_buttons.all()
    assert len(all_delete_buttons) == 2, (
        f"Should have exactly 2 delete buttons for 2 KDMAs, got {len(all_delete_buttons)}"
    )

    disabled_states = [btn.is_disabled() for btn in all_delete_buttons]
    print(f"Delete buttons disabled states: {disabled_states}")

    # Expected behavior: exactly one delete button enabled, one disabled
    # The merit KDMA should be deletable (disabled=False, leaving affiliation alone)
    # The affiliation KDMA should NOT be deletable (disabled=True, merit alone doesn't exist for this scenario)
    enabled_count = sum(1 for disabled in disabled_states if not disabled)
    disabled_count = sum(1 for disabled in disabled_states if disabled)

    assert enabled_count == 1, (
        f"Expected exactly 1 enabled delete button for June2025-AF-train scenario, but got {enabled_count} enabled buttons: {disabled_states}"
    )
    assert disabled_count == 1, (
        f"Expected exactly 1 disabled delete button for June2025-AF-train scenario, but got {disabled_count} disabled buttons: {disabled_states}"
    )

    print("✓ Correctly identified asymmetric KDMA deletion: one deletable, one not")


def test_kdma_add_remove_updates_experiment_results(page, real_data_test_server):
    """Test that adding/removing KDMAs actually updates the displayed experiment results."""
    page.goto(real_data_test_server)

    # Wait for table to load
    page.wait_for_selector(".comparison-table", timeout=10000)
    page.wait_for_function(
        "document.querySelectorAll('.table-adm-select').length > 0", timeout=10000
    )

    # Select pipeline_baseline ADM to enable KDMA functionality
    adm_select = page.locator(".table-adm-select").first
    adm_select.select_option("pipeline_baseline")
    page.wait_for_load_state("networkidle")

    # Select June2025-AF-train scenario to get multi-KDMA support
    scenario_select = page.locator(".table-scenario-select").first
    scenario_options = scenario_select.locator("option").all()
    scenario_values = [
        opt.get_attribute("value")
        for opt in scenario_options
        if opt.get_attribute("value")
    ]

    # Find a June2025-AF-train scenario (required for this test)
    june_scenarios = [s for s in scenario_values if "June2025-AF-train" in s]
    assert len(june_scenarios) > 0, (
        f"June2025-AF-train scenarios required for this test, but only found: {scenario_values}"
    )

    scenario_select.select_option(june_scenarios[0])
    page.wait_for_load_state("networkidle")

    # Get initial results content (should be single KDMA - affiliation)
    def get_results_content():
        """Helper to get the current experiment results content."""
        # Look for ADM decision or justification content
        justification_cells = page.locator('tr[data-category="justification"] td').all()
        if len(justification_cells) > 1:
            # Get the content of the first data cell (not the parameter name cell)
            content = justification_cells[1].text_content()
            return content.strip() if content else ""
        return ""

    # Wait for initial results to load
    page.wait_for_timeout(2000)
    initial_results = get_results_content()
    print(f"Initial results (single KDMA): {initial_results[:100]}...")

    # Ensure we have some initial content
    assert initial_results, "Should have initial experiment results"

    # Add a second KDMA
    add_kdma_button = page.locator(".add-kdma-btn")
    assert add_kdma_button.count() > 0, (
        "Add KDMA button must be available for this test"
    )

    add_kdma_button.click()

    # Wait for new KDMA slider to be added
    page.wait_for_function(
        "document.querySelectorAll('.table-kdma-value-slider').length > 1", timeout=5000
    )

    # Wait for results to reload (the reloadPinnedRun call should update results)
    page.wait_for_timeout(3000)  # Give time for async reload

    # Get results after adding KDMA
    multi_kdma_results = get_results_content()
    print(f"Results after adding KDMA: {multi_kdma_results[:100]}...")

    # Results should be different after adding KDMA (different experiment data)
    assert multi_kdma_results != initial_results, (
        f"Experiment results should change after adding KDMA. "
        f"Initial: '{initial_results[:50]}...' vs Multi-KDMA: '{multi_kdma_results[:50]}...'"
    )

    # Now remove a KDMA (find an enabled delete button)
    delete_buttons = page.locator(".table-kdma-remove-btn")
    assert delete_buttons.count() >= 2, "Should have delete buttons for multiple KDMAs"

    # Find an enabled delete button
    enabled_button = None
    for i in range(delete_buttons.count()):
        btn = delete_buttons.nth(i)
        if not btn.is_disabled():
            enabled_button = btn
            break

    assert enabled_button is not None, "Should have at least one enabled delete button"

    # Click the enabled delete button
    enabled_button.click()

    # Wait for KDMA to be removed
    page.wait_for_function(
        "document.querySelectorAll('.table-kdma-value-slider').length === 1",
        timeout=5000,
    )

    # Wait for results to reload after removal
    page.wait_for_timeout(3000)  # Give time for async reload

    # Get results after removing KDMA
    final_results = get_results_content()
    print(f"Results after removing KDMA: {final_results[:100]}...")

    # Results should be different from multi-KDMA results
    assert final_results != multi_kdma_results, (
        f"Experiment results should change after removing KDMA. "
        f"Multi-KDMA: '{multi_kdma_results[:50]}...' vs Final: '{final_results[:50]}...'"
    )

    # Final results might be same as initial (if we're back to single KDMA)
    # but they could also be different if the remaining KDMA is different
    print("✓ Experiment results correctly updated when adding/removing KDMAs")


def test_add_kdma_button_always_visible(page, real_data_test_server):
    """Test that Add KDMA button is always visible but gets disabled when no more KDMAs can be added."""
    page.goto(real_data_test_server)

    # Wait for table to load
    page.wait_for_selector(".comparison-table", timeout=10000)
    page.wait_for_function(
        "document.querySelectorAll('.table-adm-select').length > 0", timeout=10000
    )

    # Select pipeline_baseline ADM to enable KDMA functionality
    adm_select = page.locator(".table-adm-select").first
    adm_select.select_option("pipeline_baseline")
    page.wait_for_load_state("networkidle")

    # Select June2025-AF-train scenario to get multi-KDMA support
    scenario_select = page.locator(".table-scenario-select").first
    scenario_options = scenario_select.locator("option").all()
    scenario_values = [
        opt.get_attribute("value")
        for opt in scenario_options
        if opt.get_attribute("value")
    ]

    # Find a June2025-AF-train scenario (required for this test)
    june_scenarios = [s for s in scenario_values if "June2025-AF-train" in s]
    assert len(june_scenarios) > 0, (
        f"June2025-AF-train scenarios required for this test, but only found: {scenario_values}"
    )

    scenario_select.select_option(june_scenarios[0])
    page.wait_for_load_state("networkidle")

    # Check that Add KDMA button is visible and enabled initially
    add_kdma_button = page.locator(".add-kdma-btn")
    assert add_kdma_button.count() > 0, "Add KDMA button should always be visible"

    initial_disabled = add_kdma_button.is_disabled()
    print(f"Initial Add KDMA button disabled: {initial_disabled}")

    # For June2025-AF-train with pipeline_baseline, we should be able to add KDMAs initially
    assert not initial_disabled, "Add KDMA button should be enabled initially"

    # Add a KDMA
    add_kdma_button.click()

    # Wait for KDMA to be added
    page.wait_for_function(
        "document.querySelectorAll('.table-kdma-value-slider').length > 1", timeout=5000
    )

    # Check that Add KDMA button is still visible
    updated_add_button = page.locator(".add-kdma-btn")
    assert updated_add_button.count() > 0, (
        "Add KDMA button should still be visible after adding KDMA"
    )

    # Check if it's disabled (depends on how many KDMA types are available)
    after_add_disabled = updated_add_button.is_disabled()
    print(f"Add KDMA button disabled after adding one: {after_add_disabled}")

    # The button should now be disabled since we've likely reached the limit for this scenario
    # (pipeline_baseline typically supports only affiliation+merit combination)
    assert after_add_disabled, (
        "Add KDMA button should be disabled when no more KDMA types can be added"
    )

    # Verify tooltip is present when disabled
    tooltip = updated_add_button.get_attribute("title")
    assert tooltip, (
        "Disabled Add KDMA button should have a tooltip explaining why it's disabled"
    )
    print(f"Disabled button tooltip: {tooltip}")

    # Tooltip should explain why it's disabled
    assert (
        "available" in tooltip.lower()
        or "maximum" in tooltip.lower()
        or "reached" in tooltip.lower()
    ), f"Tooltip should explain why button is disabled, got: {tooltip}"

    print(
        "✓ Add KDMA button correctly stays visible and shows appropriate enabled/disabled state"
    )
