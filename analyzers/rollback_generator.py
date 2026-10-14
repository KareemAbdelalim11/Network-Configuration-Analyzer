def generate_rollback(

    issues
):

    rollback = []

    for issue in issues:

        # Missing VLAN

        if "VLAN 20 missing" in issue:

            rollback.append(

                "interface FastEthernet0/23"
            )

            rollback.append(

                "switchport trunk allowed vlan add 20"
            )

        # Native VLAN mismatch

        if "Native VLAN mismatch" in issue:

            rollback.append(

                "Verify native VLAN "

                "configuration on both "

                "ends of the trunk"
            )

        # Missing SVI

        if "Missing SVI" in issue:

            rollback.append(

                "Create router subinterface "

                "with encapsulation dot1Q"
            )

        # Duplicate IP

        if "Duplicate gateway IP" in issue:

            rollback.append(

                "Reassign unique gateway IPs"
            )

    return list(set(rollback))