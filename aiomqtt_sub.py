import asyncio
import aiomqtt

# async def run(topic):
#     async def main(topic):
#         try:
#             # Cancel the listener task after 5 seconds
#             async with asyncio.timeout(10):
#                 async with aiomqtt.Client("localhost")as client:
#                     await client.subscribe(topic)
#                     async for message in client.messages:
#                         print(message.payload)
#         # Ignore the resulting TimeoutError
#         except asyncio.TimeoutError:
#             pass
#     # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     # asyncio.run(main(topic))  

# async def listen(topic):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     async with aiomqtt.Client(
#         hostname="localhost",
#         port=1883,
#         username="ufanet_bot",
#         password="supersecret123"
#     ) as client:
#         await client.subscribe(topic)
#         async for message in client.messages:
#             return(message.payload)

async def listen(topic: str):
    """
    Прослушивает MQTT-топик и возвращает первое пришедшее сообщение (или None при таймауте)
    """
    try:
        async with asyncio.timeout(60):  # ждём максимум 10 секунд
            async with aiomqtt.Client(
                hostname="localhost",
                port=1883,
                username="ufanet_bot",
                password="supersecret123",
                #client_id=f"ufanet-listener-{asyncio.get_running_loop().time():.0f}"
            ) as client:
                await client.subscribe(topic)
                print(f"[MQTT] Подписались на {topic}")
                async for message in client.messages:
                    payload = message.payload.decode()
                    print(f"[MQTT] Получено из {topic}: {payload}")
                    return payload
    except asyncio.TimeoutError:
        print(f"[MQTT] Таймаут при ожидании сообщения из {topic}")
        return None
    except Exception as e:
        print(f"[MQTT] Ошибка подключения: {e}")
        return None

async def listen_once(topic: str, timeout: int = 15) -> str | None:
    """
    Подключается к MQTT, подписывается на topic,
    ждёт одно сообщение (до timeout секунд) и возвращает его.
    """
    try:
        # Поддержка и старых, и новых версий aiomqtt
        client_kwargs = {
            "hostname": "localhost",
            "port": 1883,
            "username": "ufanet_bot",
            "password": "supersecret123",
        }
        # В новых версиях — client_id, в старых — identifier
        try:
            # Попробуем новую версию
            client_kwargs["client_id"] = f"ufanet-{topic}-{id(asyncio.get_running_loop()) % 10000}"
        except TypeError:
            # Если упало — значит старая версия, используем identifier
            client_kwargs["identifier"] = f"ufanet-{topic}-{id(asyncio.get_running_loop()) % 10000}"

        async with asyncio.timeout(timeout):
            async with aiomqtt.Client(**client_kwargs) as client:
                await client.subscribe(topic)
                print(f"[MQTT] Подписались на {topic}, ждём сообщение...")
                async for message in client.messages:
                    payload = message.payload.decode("utf-8", errors="ignore")
                    print(f"[MQTT] Получено из {topic}: {payload}")
                    return payload

    except asyncio.TimeoutError:
        print(f"[MQTT] Таймаут {timeout}с — ничего не пришло на {topic}")
        return None
    except Exception as e:
        print(f"[MQTT] Ошибка подключения к {topic}: {e}")
        return None

async def main(topic):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        # Cancel the listener task after 5 seconds
        async with asyncio.timeout(15):
            msg = await listen(topic)
            return msg
        

    # Ignore the resulting TimeoutError
    
    except asyncio.TimeoutError:
        
        pass
    # return False

# topic = "mac1"
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(main(topic))

if __name__ == "__main__":
    asyncio.run(main("test/topic"))