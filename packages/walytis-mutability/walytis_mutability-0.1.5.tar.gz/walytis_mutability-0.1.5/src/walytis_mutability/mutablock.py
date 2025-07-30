from __future__ import annotations
from typing import Generic, Type, TypeVar
from decorate_all import decorate_all_functions
from strict_typing import strictly_typed
from dataclasses import dataclass
from datetime import datetime
from walytis_beta_tools._experimental.block_lazy_loading import BlocksList, BlockNotFoundError
from walytis_beta_api._experimental.generic_blockchain import  GenericBlock
from brenthy_tools_beta.utils import bytes_to_string
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mutablockchain import MutaBlockchain  # Only imported for type checking


ORIGINAL_BLOCK = "MutaBlock-Original"
UPDATE_BLOCK = "MutaBlock-Update"
DELETION_BLOCK = "MutaBlock-Deletion"

BLOCK_TYPES = {ORIGINAL_BLOCK, UPDATE_BLOCK, DELETION_BLOCK}


class MutaBlock(GenericBlock):

    def __init__(self, base_block: GenericBlock, walytis_mutability: 'MutaBlockchain'):
        self.mutablockchain: 'MutaBlockchain' = walytis_mutability
        self.base_block = base_block

    @classmethod
    def from_id(cls, block_id: bytearray, walytis_mutability: 'MutaBlockchain') -> MutaBlock:
        block = walytis_mutability.base_blockchain.get_block(block_id)
        return cls(block, walytis_mutability)

    def get_content_versions(self):
        return self.mutablockchain.get_mutablock_content_versions(self.long_id)

    def get_content_version_ids(self):
        return self.mutablockchain.get_mutablock_content_version_ids(self.long_id)

    def get_current_content_version(self) -> dict:
        """Get the compilation of the multiple ContentVersion's content."""
        return self.get_content_versions()[-1]

    def edit(self, content: bytes) -> None:
        self.mutablockchain.edit_block(
            self.get_content_version_ids()[-1],
            content
        )

    def delete(self) -> None:
        self.mutablockchain.delete_block(self.get_content_version_ids()[-1])

    @property
    def ipfs_cid(self):
        return self.base_block.ipfs_cid

    @property
    def short_id(self):
        return self.base_block.short_id

    @property
    def long_id(self):
        return self.base_block.long_id

    @property
    def creator_id(self):
        return self.base_block.creator_id

    @property
    def creation_time(self):
        return self.base_block.creation_time

    @property
    def topics(self):
        return self.base_block.topics[1:]

    @property
    def content(self):
        return self.get_current_content_version().content

    @property
    def parents(self):
        return self.base_block.parents

    @property
    def file_data(self):
        return self.base_block.file_data


@dataclass
class ContentVersion:
    type: str
    cv_id: bytearray | bytes  # same as the block ID that created this content version
    parent_id: bytearray | bytes
    original_id: bytearray | bytes
    content: bytearray | bytes
    timestamp: datetime
    topics: list[str]


# a type variable restricted to subclasses of Block
BlockType = TypeVar('BlockType', bound=MutaBlock)


class MutaBlocksList(BlocksList[BlockType]):
    def __init__(self, blockchain: 'MutaBlockchain', block_class: Type[BlockType] = MutaBlock):
        BlocksList.__init__(self, block_class)
        self.blockchain = blockchain

    @classmethod
    def from_block_ids(
        cls: Type['BlocksList[BlockType]'],
        block_ids: list[bytes],
        blockchain: 'MutaBlockchain',
        block_class: Type[BlockType] = MutaBlock
    ) -> 'BlocksList[BlockType]':

        if block_ids and bytearray([0, 0, 0, 0]) not in bytearray(block_ids[0]):
            print(block_ids[0])
            raise ValueError(
                "It looks like you passed an short ID or invalid ID as a parameter.")
        if block_ids and isinstance(block_ids[0], bytearray):
            block_ids = [bytes(block_id) for block_id in block_ids]
        # Use dict.fromkeys() to create the dictionary efficiently
        blocks_dict = dict.fromkeys(block_ids, None)

        # Cast the dictionary to an instance of BlocksList
        blocks_list = cls.__new__(cls)  # Create an uninitialized instance of the class

        # Manually initialize the dictionary part with the data
        blocks_list.update(blocks_dict)

        # Manually set the block_class
        blocks_list.block_class = block_class
        blocks_list.blockchain = blockchain

        return blocks_list

    def __getitem__(self,  block_id: bytes) -> BlockType:
        try:
            block: BlockType = dict.__getitem__(self, block_id)
        except KeyError:
            if bytearray([0, 0, 0, 0]) not in block_id:
                raise ValueError(
                    "It looks like you passed an short ID or invalid ID as a parameter.")
            else:
                raise BlockNotFoundError()
        if not block:
            block = self.block_class.from_id(bytearray(block_id), self.blockchain)
            dict.__setitem__(self, block_id, block)
        return block


decorate_all_functions(strictly_typed, __name__)
