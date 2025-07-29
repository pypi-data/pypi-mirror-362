import asyncio
from tqdm.asyncio import tqdm_asyncio
from typing import List, Optional



class ImageTextExtractor:
    def __init__(
        self,
        client,
        model: str = "gemini-2.0-flash",
        prompt: Optional[str] = None
    ):
        self.client = client
        self.model = model
        self.prompt = prompt or "Extract all text from this image:"

    async def extract_document_text(self, image, prompt: Optional[str] = None) -> str:
        effective_prompt = prompt or self.prompt
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=[effective_prompt, image]
        )
        return response.text.strip()

    async def process_images(
        self,
        images: List,
        batch_size: int = 30
        # prompt: Optional[str] = None
    ) -> List[str]:
        results = []

        for i in tqdm_asyncio(range(0, len(images), batch_size), desc="OCR images (batches)"):
            batch = images[i:i + batch_size]
            tasks = [
                self.extract_document_text(image, prompt=self.prompt)
                for image in batch
            ]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)

        return results