# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s rer.pubblicazioni -t test_pubblicazione.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src rer.pubblicazioni.testing.RER_PUBBLICAZIONI_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_pubblicazione.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Pubblicazione
  Given a logged-in site administrator
    and an add pubblicazione form
   When I type 'My Pubblicazione' into the title field
    and I submit the form
   Then a pubblicazione with the title 'My Pubblicazione' has been created

Scenario: As a site administrator I can view a Pubblicazione
  Given a logged-in site administrator
    and a pubblicazione 'My Pubblicazione'
   When I go to the pubblicazione view
   Then I can see the pubblicazione title 'My Pubblicazione'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add pubblicazione form
  Go To  ${PLONE_URL}/++add++Pubblicazione

a pubblicazione 'My Pubblicazione'
  Create content  type=Pubblicazione  id=my-pubblicazione  title=My Pubblicazione


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the pubblicazione view
  Go To  ${PLONE_URL}/my-pubblicazione
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a pubblicazione with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the pubblicazione title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
