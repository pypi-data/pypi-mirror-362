from ..client.game_client import GameClient
import asyncio
from loguru import logger
from typing import Any
import contextlib
import inspect



class Map(GameClient):
    
    
    async def get_map_chunks_as(self, kingdom, x, y):
        
        try:
            
            await self.send_json_message("gaa",{
                "KID": kingdom,
                "AX1": x,
                "AY1": y,
                "AX2": x + 12,
                "AY2": y + 12
            })
            
            
            
        except Exception as e:
            logger.error(e)
            return False
    
    
    
    
    async def get_map_chunks_sync(
        self,
        kingdom: int,
        x: int,
        y: int,
        sync: bool = True
    ) -> dict | bool:
        
        try:
            await self.send_json_message(
                "gaa",
                {
                    "KID": kingdom,
                    "AX1": x,
                    "AY1": y,
                    "AX2": x + 12,
                    "AY2": y + 12
                    
                }
            )
            if sync:
                response = await self.wait_for_response("gaa")
                return response
            return True
        
        except Exception as e:
            logger.error(e)
            return False
    
    
    
    
    
    
    async def get_closest_npc(
        self,
        kingdom: int,
        npc_type: int,
        min_level: int = 1,
        max_level: int = -1,
        owner_id: int = -1,
        sync: bool = True
        ) -> dict | bool:
        
        try:
            await self.send_json_message(
                "fnm",
                {
                    
                    "T": npc_type,
                    "KID": kingdom,
                    "LMIN": min_level,
                    "LMAX": max_level,
                    "NID": owner_id
                }
            )
            if sync:
                response = await self.wait_for_response("fnm")
                return response
            return True
            
        except Exception as e:
            logger.error(e)
            return False
        
        

    
    def _spiral_coords(self, max_radius: int, cx: int, cy: int):
        step = 13
        seen = set()
        for radius in range(step, max_radius + 1, step):

            for x in range(cx - radius, cx + radius + 1, step):
                pt = (x, cy - radius)
                if pt not in seen:
                    seen.add(pt)
                    yield pt
           
            for y in range(cy - radius, cy + radius + 1, step):
                pt = (cx + radius, y)
                if pt not in seen:
                    seen.add(pt)
                    yield pt
            
            for x in range(cx + radius, cx - radius - 1, -step):
                pt = (x, cy + radius)
                if pt not in seen:
                    seen.add(pt)
                    yield pt
           
            for y in range(cy + radius, cy - radius - 1, -step):
                pt = (cx - radius, y)
                if pt not in seen:
                    seen.add(pt)
                    yield pt
        
        seen.clear()
    
    
    
    
    
    
    async def map_scanner(
        self,
        kingdom: int,
        max_radius: int,
        castle_x: int,
        castle_y: int,
        handler: Any
        ):

        
        processing_task = asyncio.create_task(
            self.process_data("gaa", handler, interval=0.5)
        )
        try:
            logger.info("Scanning...")
            
            for x, y in self._spiral_coords(max_radius=max_radius, cx=castle_x, cy=castle_y):
                await self.get_map_chunks_as(kingdom, x, y)
                await asyncio.sleep(0.01)
            logger.info("Complete")
        finally:
            
            processing_task.cancel()
            
            
     
     
            
    async def find_by_name(
        self,
        user_name: str,
        sync: bool = True
    ) -> dict | bool:
        
        try:
            await self.send_json_message("wsp", {"PN": user_name})
            if sync:
                response = await self.wait_for_response("wsp")
                return response
            return True
        
        except Exception as e:
            logger.error(e)
            return False
        
    
    
    async def get_npc_target_infos(
        self,
        tx: int,
        ty: int,
        sx: int,
        sy: int,
        kid: int,
        sync: bool = True
    ) -> dict | bool:
        
        try:
            await self.send_json_message(
                "adi",
                {
                    "TX": tx,
                    "TY": ty,
                    "SX": sx,
                    "SY": sy,
                    "KID": kid
                }
            )
            if sync:
                response = await self.wait_for_response("adi")
                return response
            return True
        
        except Exception as e:
            logger.error(e)
            return False
        




    async def get_pvp_target_infos(
        self,
        tx: int,
        ty: int,
        sx: int,
        sy: int,
        kid: int,
        sync: bool = True
    ) -> dict | bool:
        
        try:
            await self.send_json_message(
                "aci",
                {
                    "TX": tx,
                    "TY": ty,
                    "SX": sx,
                    "SY": sy,
                    "KID": kid
                }
            )
            if sync:
                response = await self.wait_for_response("aci")
                return response
            return True
        
        except Exception as e:
            logger.error(e)
            return False
        
        
        
    async def map_multi_scanner(
        self,
        kingdom: int,
        max_radius: int,
        castle_x: int,
        castle_y: int,
        handler: Any,
        interval: float
        ) -> None:
        
        while True:
            
            processing_task = asyncio.create_task(
                self.process_data("gaa", handler, interval=0.5)
            )
            try:
                logger.info("Starting scan")
                for x, y in self._spiral_coords(max_radius, castle_x, castle_y):
                    await self.get_map_chunks_as(kingdom, x, y)
                    await asyncio.sleep(0.01)
                logger.info("Scan complete!")
                
            finally:
                processing_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await processing_task
                    
            logger.info("Sleeping until start next scan", interval)
            await asyncio.sleep(interval)
                    

    async def bulk_multi_scanner(
        self,
        kingdom: int,
        max_radius: int,
        castle_x: int,
        castle_y: int,
        handler: Any,
        interval: float = 15.0
    ) -> None:
        
        while True:
            
            data_list: list[dict] = []
            coords = list(self._spiral_coords(max_radius, castle_x, castle_y))
            tasks = [
                self.get_map_chunks_sync(kingdom, x, y, sync=True)
                for x, y in coords
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for resp in results:
                if isinstance(resp, dict):
                    data_list.append(resp)
                
                else:
                    logger.warning(f"Fetch error: {resp}")
            
            try:
                maybe_await = handler(data_list)
                if inspect.isawaitable(maybe_await):
                    await maybe_await
                    
            except Exception as e:
                logger.error(f"Handler error: {e}")
            
            await asyncio.sleep(interval)


    


