
Feature: Standard DHCPv6 message types
    This is a simple DHCPv6 message exchange validation. Its purpose is to check if presence of message types from RFC 3315 section 5.3
@basic
    Scenario: v6.basic.message.advertise

    	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	References: RFC3315 section 5.3
@basic
    Scenario: v6.basic.message.request-reply

    	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
@basic
    Scenario: v6.basic.message.confirm-reply
#nie dziala, nie wspierane!
    	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
@basic
    Scenario: v6.basic.message.renew-reply

    	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
@basic	
    Scenario: v6.basic.message.rebind-reply
#nie dziala, nie wspierane!
    	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
@basic
    Scenario: v6.basic.message.release-reply

    	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
@basic
    Scenario: v6.basic.message.decline-reply
#decline tez nie wspierany, ale test dziala
    	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
@basic
    Scenario: v6.basic.message.information_request-reply

    	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends INFREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

