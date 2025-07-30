#################################################################################
# Eclipse Tractus-X - Software Development KIT
#
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the
# License for the specific language govern in permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
#################################################################################
## Code created partially using a LLM (GPT 4o) and reviewed by a human committer

from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import JSON
from sqlmodel import Column
from ..base_connection_manager import BaseConnectionManager
from sqlalchemy.engine import Engine as E
from sqlalchemy.orm import Session as S

# SQLModel model for EDRConnection
class EDRConnection(SQLModel, table=True):
    __tablename__ = "edr_connections"

    transfer_id: str = Field(primary_key=True)
    counter_party_id: str
    counter_party_address: str
    query_checksum: str
    policy_checksum: str
    edr_data: dict = Field(sa_column=Column(JSON))


class PostgresConnectionManager(BaseConnectionManager):
    def __init__(self, engine: E | S):
        self.engine = engine
        EDRConnection.metadata.create_all(engine)
        
    def add_connection(self, counter_party_id: str, counter_party_address: str, query_checksum: str, policy_checksum: str, connection_entry: dict) -> str | None:
        transfer_process_id: str = connection_entry.get(self.TRANSFER_ID_KEY, None)
        if not transfer_process_id:
            raise Exception("[Postgres Connection Manager] The transfer id key was not found or is empty! Not able to do the contract negotiation!")

        saved_edr = connection_entry.copy()
        saved_edr.pop("@type", None)
        saved_edr.pop("providerId", None)
        saved_edr.pop("@context", None)

        new_entry = EDRConnection(
            counter_party_id=counter_party_id,
            counter_party_address=counter_party_address,
            query_checksum=query_checksum,
            policy_checksum=policy_checksum,
            transfer_id=transfer_process_id,
            edr_data=saved_edr
        )

        with Session(self.engine) as session:
            if not session.get(EDRConnection, transfer_process_id):
                session.add(new_entry)
                session.commit()
                print("[Postgres Connection Manager] A new EDR entry was saved in the database.")
        return transfer_process_id

    def get_connection(self, counter_party_id, counter_party_address, query_checksum, policy_checksum):
        stmt = select(EDRConnection).where(
            EDRConnection.counter_party_id == counter_party_id,
            EDRConnection.counter_party_address == counter_party_address,
            EDRConnection.query_checksum == query_checksum,
            EDRConnection.policy_checksum == policy_checksum
        )
        with Session(self.engine) as session:
            result = session.exec(stmt).first()
        return result.edr_data if result else {}

    def get_connection_transfer_id(self, counter_party_id, counter_party_address, query_checksum, policy_checksum):
        stmt = select(EDRConnection.transfer_id).where(
            EDRConnection.counter_party_id == counter_party_id,
            EDRConnection.counter_party_address == counter_party_address,
            EDRConnection.query_checksum == query_checksum,
            EDRConnection.policy_checksum == policy_checksum
        )
        with Session(self.engine) as session:
            result = session.exec(stmt).first()
        return result if result else None

    def delete_connection(self, counter_party_id: str, counter_party_address: str, query_checksum: str, policy_checksum: str) -> bool:
        stmt = select(EDRConnection).where(
            EDRConnection.counter_party_id == counter_party_id,
            EDRConnection.counter_party_address == counter_party_address,
            EDRConnection.query_checksum == query_checksum,
            EDRConnection.policy_checksum == policy_checksum
        )
        with Session(self.engine) as session:
            result = session.exec(stmt).first()
            if result:
                session.delete(result)
                session.commit()
                print(f"[Postgres Connection Manager] Deleted EDR entry for policy checksum '{policy_checksum}'.")
                return True
            else:
                print(f"[Postgres Connection Manager] No EDR found to delete for the provided keys.")
                return False