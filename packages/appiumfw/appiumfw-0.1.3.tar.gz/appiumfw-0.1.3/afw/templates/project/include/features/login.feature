Feature: Sauce Labs APK Mobile Login
  @positive
  Scenario: Successful login on Sauce Labs Android emulator
    Given the mobile app is installed on Sauce Labs device
    When the user enters username "standard_user" and password "secret_sauce"
    And the user taps the login button
    Then the home screen should be displayed