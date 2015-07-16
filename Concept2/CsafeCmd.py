"""
PyRow.Concept2.CsafeCmd
"""
# coding=utf-8
# Copyright (c) 2011, Sam Gambrell,
# Licensed under the Simplified BSD License.
__author__ = 'Sam Gambrell and UVD'

#ToDo: change print statments to proper errors

import PyRow.csafe_dic as csafe_dic


class CsafeCmd:
    """
    CsafeCmd
    """

    @staticmethod
    def __int2bytes(num_bytes, integer):
        """
        :param num_bytes:
        :param integer:
        :return:
        """
        if not 0 <= integer <= 2 ** (8 * num_bytes):
            print "Integer is outside the allowable range"

        byte = []
        for k in range(num_bytes):
            calc_byte = (integer >> (8 * k)) & 0xFF
            byte.append(calc_byte)

        return byte

    @staticmethod
    def __bytes2int(raw_bytes):
        """
        :param raw_bytes:
        :return:
        """
        num_bytes = len(raw_bytes)
        integer = 0

        for k in range(num_bytes):
            integer = (raw_bytes[k] << (8 * k)) | integer

        return integer

    @staticmethod
    def __bytes2ascii(raw_bytes):
        """
        :param raw_bytes:
        :return:
        """
        word = ""
        for letter in raw_bytes:
            word += chr(letter)

        return word

    @staticmethod
    def write(arguments):
        """
        :param arguments:
        :return:
        """
        # Priming variables
        i = 0
        message = []
        wrapper = 0
        wrapped = []
        max_response = 3  # Start & stop flag & status

        # Loop through all arguments
        while i < len(arguments):

            arg = arguments[i]
            cmd_prop = csafe_dic.cmds[arg]
            command = []

            # Load variables if command is a Long Command
            if len(cmd_prop[1]) != 0:
                for varbytes in cmd_prop[1]:
                    i += 1
                    intvalue = arguments[i]
                    value = CsafeCmd.__int2bytes(varbytes, intvalue)
                    command.extend(value)

                # Data byte count
                cmd_bytes = len(command)
                command.insert(0, cmd_bytes)

            # Add command ID
            command.insert(0, cmd_prop[0])

            # Closes wrapper if required
            if len(wrapped) > 0 and (len(cmd_prop) < 3 or cmd_prop[2] != wrapper):
                wrapped.insert(0, len(wrapped))  # Data byte count for wrapper
                wrapped.insert(0, wrapper)  # Wrapper command id
                message.extend(wrapped)  # Adds wrapper to message
                wrapped = []
                wrapper = 0

            # Create or extend wrapper
            if len(cmd_prop) == 3:  # Checks if command needs a wrapper
                if wrapper == cmd_prop[2]:  # Checks if currently in the same wrapper
                    wrapped.extend(command)
                else:  # Creating a new wrapper
                    wrapped = command
                    wrapper = cmd_prop[2]
                    max_response += 2

                command = []  # Clear command to prevent it from getting into message

            # Max message length
            cmd_id = cmd_prop[0] | (wrapper << 8)
            # Double return to account for stuffing
            max_response += abs(sum(csafe_dic.resp[cmd_id][1])) * 2 + 1

            # Add completed command to final message
            message.extend(command)

            i += 1

        # Closes wrapper if message ended on it
        if len(wrapped) > 0:
            wrapped.insert(0, len(wrapped))  # Data byte count for wrapper
            wrapped.insert(0, wrapper)  # Wrapper command ID
            message.extend(wrapped)  # Adds wrapper to message

        # Prime variables
        checksum = 0x0
        j = 0

        # Checksum and byte stuffing
        while j < len(message):
            # Calculate checksum
            checksum = checksum ^ message[j]

            # Byte stuffing
            if 0xF0 <= message[j] <= 0xF3:
                message.insert(j, csafe_dic.Byte_Stuffing_Flag)
                j += 1
                message[j] &= 0x3

            j += 1

        # Add checksum to end of message
        message.append(checksum)

        # Start & stop frames
        message.insert(0, csafe_dic.Standard_Frame_Start_Flag)
        message.append(csafe_dic.Stop_Frame_Flag)

        # Check for frame size (96 bytes)
        if len(message) > 96:
            print "Message is too long: {0}".format(len(message))

        # Report IDs
        max_message = max(len(message) + 1, max_response)

        if max_message <= 21:
            message.insert(0, 0x01)
            message += [0] * (21 - len(message))
        elif max_message <= 63:
            message.insert(0, 0x04)
            message += [0] * (63 - len(message))
        elif (len(message) + 1) <= 121:
            message.insert(0, 0x02)
            message += [0] * (121 - len(message))
            if max_response > 121:
                print "Response may be too long to recieve.  Max possible length " + str(max_response)
        else:
            print "Message too long.  Message length " + str(len(message))
            message = []

        return message

    @staticmethod
    def __check_message(message):
        """
        :param message:
        :return:
        """
        # Prime variables
        i = 0
        checksum = 0

        # Checksum and unstuff
        while i < len(message):
            # Byte unstuffing
            if message[i] == csafe_dic.Byte_Stuffing_Flag:
                stuff_value = message.pop(i + 1)
                message[i] = 0xF0 | stuff_value

            # Calculate checksum
            checksum = checksum ^ message[i]

            i += 1

        # Checks checksum
        if checksum != 0:
            print "Checksum error"
            return []

        # Remove checksum from  end of message
        del message[-1]

        return message

    # For receiving!
    @staticmethod
    def read(transmission):
        """
        :param transmission:
        :return:
        """
        # Prime variables
        message = []
        stop_found = False

        # Report ID = transmission[0]
        start_flag = transmission[1]

        if start_flag == csafe_dic.Extended_Frame_Start_Flag:
            # Destination = transmission[2]
            # Source = transmission[3]
            j = 4
        elif start_flag == csafe_dic.Standard_Frame_Start_Flag:
            j = 2
        else:
            print "No Start Flag found."
            return []

        while j < len(transmission):
            if transmission[j] == csafe_dic.Stop_Frame_Flag:
                stop_found = True
                break
            message.append(transmission[j])
            j += 1

        if not stop_found:
            print "No Stop Flag found."
            return []

        message = CsafeCmd.__check_message(message)
        status = message.pop(0)

        # Prime variables
        response = {'CSAFE_GETSTATUS_CMD': [status, ]}
        k = 0
        wrap_end = -1
        wrapper = 0x0

        # Loop through complete frames
        while k < len(message):
            result = []

            # Get command name
            msg_cmd = message[k]
            if k <= wrap_end:
                msg_cmd |= wrapper  # Check if still in wrapper
            msg_prop = csafe_dic.resp[msg_cmd]
            k += 1

            # Get data byte count
            byte_count = message[k]
            k += 1

            # If wrapper command then gets command in wrapper
            if msg_prop[0] == 'CSAFE_SETUSERCFG1_CMD':
                wrapper = message[k - 2] << 8
                wrap_end = k + byte_count - 1
                if byte_count:  # If wrapper length != 0
                    msg_cmd = wrapper | message[k]
                    msg_prop = csafe_dic.resp[msg_cmd]
                    k += 1
                    byte_count = message[k]
                    k += 1

            # Special case for capability code, response lengths differ based off capability code
            if msg_prop[0] == 'CSAFE_GETCAPS_CMD':
                msg_prop[1] = [1, ] * byte_count

            # Special case for get id, response length is variable
            if msg_prop[0] == 'CSAFE_GETID_CMD':
                msg_prop[1] = [(-byte_count), ]

            # Checking that the received data byte is the expected length, sanity check
            if abs(sum(msg_prop[1])) != 0 and byte_count != abs(sum(msg_prop[1])):
                print "Warning: byte_count is an unexpected length"

            # Extract values
            for num_bytes in msg_prop[1]:
                raw_bytes = message[k:k + abs(num_bytes)]
                value = (CsafeCmd.__bytes2int(raw_bytes) if num_bytes >= 0 else CsafeCmd.__bytes2ascii(raw_bytes))
                result.append(value)
                k = k + abs(num_bytes)

            response[msg_prop[0]] = result

        return response
