# Created by Tevi at 25/02/2023
  @RUN
Feature: Images


  Scenario: Create a new image
    Given a new image
    When image is requested for download
    Then image is downloaded
    When image is sent to storage in the database

  Scenario: Get
    Given the url
    When we hit /images
    Then we obtain images