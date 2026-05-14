"""Integration tests for FastAPI backend endpoints."""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_dict(self, client):
        """Test that /activities endpoint returns a dictionary of activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_get_activities_contains_expected_activities(self, client):
        """Test that all expected activities are present."""
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Swimming Club",
            "Art Club",
            "Drama Society",
            "Math Olympiad",
            "Science Club",
        ]
        response = client.get("/activities")
        data = response.json()
        for activity_name in expected_activities:
            assert activity_name in data

    def test_get_activities_activity_structure(self, client):
        """Test that each activity has the required fields."""
        response = client.get("/activities")
        data = response.json()
        required_fields = {"description", "schedule", "max_participants", "participants"}
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys())
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_participants_are_strings(self, client):
        """Test that participants in each activity are email strings."""
        response = client.get("/activities")
        data = response.json()
        for activity_name, activity_data in data.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant  # Basic email format check


class TestRootRedirect:
    """Test suite for GET / endpoint."""

    def test_root_redirects_to_static(self, client):
        """Test that root endpoint redirects to static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newemail@mergington.edu"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newemail@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_updates_participants(self, client):
        """Test that signup actually adds the participant to the activity."""
        email = "test_participant@mergington.edu"
        # Sign up
        response = client.post(
            "/activities/Chess Club/signup", params={"email": email}
        )
        assert response.status_code == 200

        # Verify participant is added
        response = client.get("/activities")
        activities = response.json()
        assert email in activities["Chess Club"]["participants"]

    def test_signup_activity_not_found(self, client):
        """Test signup fails when activity does not exist."""
        response = client.post(
            "/activities/Non-Existent Activity/signup",
            params={"email": "student@mergington.edu"},
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_email(self, client):
        """Test signup fails when student is already signed up."""
        email = "michael@mergington.edu"  # Already in Chess Club
        response = client.post(
            "/activities/Chess Club/signup", params={"email": email}
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_different_activity(self, client):
        """Test that signup to a different activity works for already-signed-up student."""
        email = "michael@mergington.edu"  # Already in Chess Club
        # Should be able to sign up for a different activity
        response = client.post(
            "/activities/Programming Class/signup", params={"email": email}
        )
        assert response.status_code == 200


class TestRemoveParticipant:
    """Test suite for DELETE /activities/{activity_name}/participants endpoint."""

    def test_remove_participant_success(self, client):
        """Test successful removal of a participant from an activity."""
        email = "michael@mergington.edu"
        response = client.delete(
            "/activities/Chess Club/participants", params={"email": email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Chess Club" in data["message"]

    def test_remove_participant_updates_list(self, client):
        """Test that removal actually removes the participant."""
        email = "michael@mergington.edu"
        # Remove participant
        response = client.delete(
            "/activities/Chess Club/participants", params={"email": email}
        )
        assert response.status_code == 200

        # Verify participant is removed
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities["Chess Club"]["participants"]

    def test_remove_participant_activity_not_found(self, client):
        """Test removal fails when activity does not exist."""
        response = client.delete(
            "/activities/Non-Existent Activity/participants",
            params={"email": "student@mergington.edu"},
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_remove_participant_not_found(self, client):
        """Test removal fails when participant is not in the activity."""
        response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": "nonexistent@mergington.edu"},
        )
        assert response.status_code == 404
        data = response.json()
        assert "Participant not found" in data["detail"]

    def test_remove_then_signup_again(self, client):
        """Test that a removed participant can sign up again."""
        email = "michael@mergington.edu"
        # Remove participant
        response = client.delete(
            "/activities/Chess Club/participants", params={"email": email}
        )
        assert response.status_code == 200

        # Sign up again
        response = client.post(
            "/activities/Chess Club/signup", params={"email": email}
        )
        assert response.status_code == 200

        # Verify participant is back
        response = client.get("/activities")
        activities = response.json()
        assert email in activities["Chess Club"]["participants"]
