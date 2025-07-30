import streamlit as st
import httpx

API_URL = "http://localhost:8000"

async def discover_materials(composition: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/discover", json={"composition": composition})
        response.raise_for_status()
        return response.json()