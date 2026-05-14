"""
SIMPLE TESTING EXAMPLE
Learn the basics of testing with a simple calculator function
"""

# ============================================================================
# PART 1: The Function We Want to Test
# ============================================================================

def calculate_tip_percentage(fare_amount, tip_amount):
    """
    Calculate tip percentage from fare and tip amounts.
    
    Formula: (tip / fare) * 100
    
    Example:
        fare=$10, tip=$2 → 20%
    """
    if fare_amount <= 0:
        return 0  # Avoid division by zero
    
    return (tip_amount / fare_amount) * 100


def filter_valid_trips(trips):
    """
    Filter out invalid trips.
    
    Rules:
        - fare must be > 0
        - distance must be > 0
    """
    valid_trips = []
    for trip in trips:
        fare, distance = trip["fare"], trip["distance"]
        if fare > 0 and distance > 0:
            valid_trips.append(trip)
    return valid_trips


# ============================================================================
# PART 2: Test Functions (Using pytest)
# ============================================================================

def test_tip_percentage_calculation():
    """
    Test that tip percentage is calculated correctly.
    
    ARRANGE-ACT-ASSERT Pattern:
    """
    # ARRANGE: Set up test data (GIVEN)
    fare = 10.00
    tip = 2.00
    
    # ACT: Run the function (WHEN)
    result = calculate_tip_percentage(fare, tip)
    
    # ASSERT: Check the result (THEN)
    assert result == 20.0, f"Expected 20.0 but got {result}"
    print(f"✅ Test passed: ${fare} fare + ${tip} tip = {result}%")


def test_tip_percentage_zero_fare():
    """
    Test edge case: What happens with zero fare?
    
    This is called "Edge Case Testing" - testing unusual inputs
    """
    # ARRANGE
    fare = 0.00
    tip = 2.00
    
    # ACT
    result = calculate_tip_percentage(fare, tip)
    
    # ASSERT
    assert result == 0, "Zero fare should return 0% (avoid division by zero)"
    print(f"✅ Test passed: Edge case (zero fare) handled correctly")


def test_filter_removes_invalid_trips():
    """
    Test that invalid trips are filtered out.
    
    WHAT WE'RE TESTING: Data quality filtering logic
    WHY: Ensure bad data doesn't make it to Silver layer
    """
    # ARRANGE: Create test data with invalid trips
    trips = [
        {"id": 1, "fare": 10.00, "distance": 2.5},   # Valid
        {"id": 2, "fare": -5.00, "distance": 1.0},   # Invalid: negative fare
        {"id": 3, "fare": 12.00, "distance": 0.0},   # Invalid: zero distance
        {"id": 4, "fare": 15.00, "distance": 3.2},   # Valid
    ]
    
    # ACT: Run the filter function
    valid_trips = filter_valid_trips(trips)
    
    # ASSERT: Check that only valid trips remain
    assert len(valid_trips) == 2, f"Expected 2 valid trips, got {len(valid_trips)}"
    assert valid_trips[0]["id"] == 1, "First valid trip should be ID 1"
    assert valid_trips[1]["id"] == 4, "Second valid trip should be ID 4"
    print(f"✅ Test passed: Filtered {len(trips)} trips → {len(valid_trips)} valid trips")


def test_filter_keeps_all_valid_trips():
    """
    Test that valid trips are NOT filtered out.
    
    This is called "Positive Testing" - ensuring good data passes through
    """
    # ARRANGE: All valid trips
    trips = [
        {"id": 1, "fare": 10.00, "distance": 2.5},
        {"id": 2, "fare": 12.00, "distance": 3.0},
        {"id": 3, "fare": 15.00, "distance": 1.5},
    ]
    
    # ACT
    valid_trips = filter_valid_trips(trips)
    
    # ASSERT: All should pass through
    assert len(valid_trips) == 3, "All valid trips should be kept"
    print(f"✅ Test passed: All {len(valid_trips)} valid trips kept")


# ============================================================================
# PART 3: Understanding What We Test Against
# ============================================================================

"""
WHAT ARE WE TESTING AGAINST?

1. EXPECTED BEHAVIOR (Logic)
   - Function: calculate_tip_percentage(10, 2)
   - Test Against: Expected output = 20.0
   - Why: Verify the math is correct

2. BUSINESS RULES (Requirements)
   - Function: filter_valid_trips()
   - Test Against: Fare > 0, Distance > 0
   - Why: Data quality requirements

3. EDGE CASES (Unusual Inputs)
   - Function: calculate_tip_percentage(0, 2)
   - Test Against: Should not crash (return 0)
   - Why: Handle unusual situations gracefully

4. SCHEMA/STRUCTURE (Data Format)
   - Function: Returns list of dictionaries
   - Test Against: Each dict has "id", "fare", "distance"
   - Why: Downstream systems expect this format
"""


# ============================================================================
# PART 4: Run Tests Manually (Without pytest)
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🧪 RUNNING SIMPLE TESTS")
    print("=" * 70)
    print()
    
    try:
        # Run each test
        print("Test 1: Tip Percentage Calculation")
        test_tip_percentage_calculation()
        print()
        
        print("Test 2: Edge Case - Zero Fare")
        test_tip_percentage_zero_fare()
        print()
        
        print("Test 3: Filter Invalid Trips")
        test_filter_removes_invalid_trips()
        print()
        
        print("Test 4: Keep Valid Trips")
        test_filter_keeps_all_valid_trips()
        print()
        
        print("=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED:")
        print(f"   {e}")
        print("\n💡 This means the function didn't behave as expected!")
        print("   You need to fix the function logic.")


# ============================================================================
# PART 5: Key Concepts Explained
# ============================================================================

"""
📚 KEY TESTING CONCEPTS:

1. ARRANGE-ACT-ASSERT (The 3 A's)
   
   ARRANGE: Set up test data
   --------
   fare = 10.00
   tip = 2.00
   
   ACT: Run the function
   ----
   result = calculate_tip_percentage(fare, tip)
   
   ASSERT: Check the result
   -------
   assert result == 20.0


2. POSITIVE vs NEGATIVE TESTING
   
   Positive Testing: Test with valid inputs (should work)
   ----------------
   test_filter_keeps_all_valid_trips()  # All trips are valid
   
   Negative Testing: Test with invalid inputs (should be rejected)
   ----------------
   test_filter_removes_invalid_trips()  # Some trips are invalid


3. EDGE CASE TESTING
   
   Edge Cases: Unusual/extreme inputs
   -----------
   - Zero values: calculate_tip_percentage(0, 2)
   - NULL values: calculate_tip_percentage(None, 2)
   - Very large values: calculate_tip_percentage(999999, 100000)
   - Empty lists: filter_valid_trips([])


4. ISOLATION
   
   Each test is independent:
   -------------------------
   test_1() does NOT affect test_2()
   
   ❌ BAD: Tests share data
   global_data = []
   
   def test_1():
       global_data.append(1)
   
   def test_2():
       # Depends on test_1 running first - BAD!
       assert len(global_data) == 1
   
   ✅ GOOD: Each test creates own data
   def test_1():
       data = [1, 2, 3]
       assert len(data) == 3
   
   def test_2():
       data = [4, 5]  # Independent
       assert len(data) == 2


5. ASSERT STATEMENTS
   
   Syntax: assert <condition>, "Error message"
   
   Examples:
   ---------
   assert result == 20.0
   assert len(trips) > 0
   assert "fare" in trip_dict
   assert trip.fare > 0 and trip.distance > 0
   
   If condition is False → Test FAILS
   If condition is True → Test PASSES


6. TEST NAMING
   
   Convention: test_<what>_<scenario>
   
   Good names:
   -----------
   test_tip_percentage_calculation()
   test_filter_removes_negative_fares()
   test_schema_has_required_columns()
   
   Bad names:
   ----------
   test1()  # What does this test?
   test_function()  # Which function?
   test_stuff()  # Too vague
"""


# ============================================================================
# PART 6: Try It Yourself!
# ============================================================================

"""
🎯 EXERCISE: Write Your Own Test

Function to test:
-----------------
def remove_duplicates(trips):
    seen = set()
    unique_trips = []
    for trip in trips:
        key = (trip["pickup_time"], trip["fare"])
        if key not in seen:
            unique_trips.append(trip)
            seen.add(key)
    return unique_trips


Your task: Write a test for this function
------------------------------------------

def test_remove_duplicates():
    # ARRANGE: Create test data with duplicates
    trips = [
        {"pickup_time": "10:00", "fare": 10.00},
        {"pickup_time": "10:00", "fare": 10.00},  # DUPLICATE
        {"pickup_time": "11:00", "fare": 12.00},
    ]
    
    # ACT: Run the function
    result = remove_duplicates(trips)
    
    # ASSERT: Check the result
    assert len(result) == 2, "Should have 2 unique trips (duplicate removed)"
    
    print("✅ Your test passed!")


Try running this file:
----------------------
python tests/test_simple_example.py
"""
