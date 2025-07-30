import socket
import struct
import time

def ping(host="", port=19132, timeout=5) -> dict:
    """
    Улучшенная версия пинга Bedrock сервера с обработкой неполных ответов
    """
    MAGIC = bytes.fromhex("00ffff00fefefefefdfdfdfd12345678")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)

    try:
        # Формируем Unconnected Ping
        ping_packet = (
            b'\x01'  # Packet ID
            + struct.pack('>Q', int(time.time() * 1000))  # Timestamp
            + MAGIC  # Magic
            + struct.pack('>Q', 12345678)  # Client GUID
        )
        sock.sendto(ping_packet, (host, port))

        # Получаем ответ
        data, _ = sock.recvfrom(4096)
        
        if data[0] != 0x1C:
            raise ValueError("Неверный ID ответного пакета")

        # Парсим базовые поля
        offset = 1
        server_timestamp = struct.unpack('>Q', data[offset:offset+8])[0]
        offset += 8
        server_guid = struct.unpack('>Q', data[offset:offset+8])[0]
        offset += 8
        magic = data[offset:offset+16]
        offset += 16

        if magic != MAGIC:
            raise ValueError("Неверные Magic-байты")

        # Читаем строку с информацией
        str_len = struct.unpack('>H', data[offset:offset+2])[0]
        offset += 2
        server_info = data[offset:offset+str_len].decode('utf-8').split(';')
        raw_response = ";".join(server_info)

        # Базовый словарь с информацией
        result = {
            "latency_ms": int(time.time() * 1000) - server_timestamp,
            "raw_response": raw_response,
            "server_guid": server_guid
        }

        # Пытаемся извлечь стандартные поля
        try:
            result.update({
                "edition": server_info[0] if len(server_info) > 0 else "Unknown",
                "motd_line1": server_info[1] if len(server_info) > 1 else "Unknown",
                "protocol": int(server_info[2]) if len(server_info) > 2 and server_info[2].isdigit() else 0,
                "version": server_info[3] if len(server_info) > 3 else "Unknown",
                "online_players": int(server_info[4]) if len(server_info) > 4 and server_info[4].isdigit() else 0,
                "max_players": int(server_info[5]) if len(server_info) > 5 and server_info[5].isdigit() else 0,
            })
        except Exception as e:
            print(f"Ошибка при разборе стандартных полей: {e}")

        # Дополнительные поля (могут отсутствовать)
        if len(server_info) > 6:
            result["server_id"] = server_info[6]
        if len(server_info) > 7:
            result["motd_line2"] = server_info[7]
        if len(server_info) > 8:
            result["gamemode"] = server_info[8]
        if len(server_info) > 10 and server_info[10].isdigit():
            result["port_ipv4"] = int(server_info[10])
        if len(server_info) > 11 and server_info[11].isdigit():
            result["port_ipv6"] = int(server_info[11])

        return result

    except socket.timeout:
        print("Сервер не ответил в течение заданного времени.")
        return None
    except Exception as e:
        print(f"Ошибка при запросе: {e}")
        return None
    finally:
        sock.close()
