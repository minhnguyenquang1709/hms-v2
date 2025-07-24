```python
Base = declarative_base()

class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)

sessionmanager = DatabaseSessionManager()
```

Here's an intuitive explanation of the `DatabaseSessionManager` class:

### 🧠 Core Purpose

Manages database connections and sessions for async SQLAlchemy applications. It handles:

1. Connection pooling
2. Session lifecycle
3. Transaction management
4. Clean resource cleanup

### 🔧 Key Components Explained

1. **Initialization**:

   ```python
   def __init__(self):
       self._engine = None
       self._sessionmaker = None
   ```

   - Creates an "empty" manager that will be configured later with `init()`

2. **Setup**:

   ```python
   def init(self, host: str):
       self._engine = create_async_engine(host)
       self._sessionmaker = async_sessionmaker(bind=self._engine)
   ```

   - "Activates" the manager with database credentials
   - Creates:
     - `_engine`: Connection pool (manages physical DB connections)
     - `_sessionmaker`: Factory for creating sessions (logical DB interactions)

3. **Connection Context Manager**:

   ```python
   async def connect(self):
       async with self._engine.begin() as connection:
           try:
               yield connection  # ← You work here
           except Exception:
               await connection.rollback()
               raise
   ```

   - Usage:
     ```python
     async with manager.connect() as conn:
         await conn.execute("SELECT 1")
     ```
   - Guarantees:
     - Auto-rollback on errors
     - Connection returned to pool when done

4. **Session Context Manager**:

   ```python
   async def session(self):
       session = self._sessionmaker()
       try:
           yield session  # ← You work here
       except Exception:
           await session.rollback()
           raise
       finally:
           await session.close()
   ```

   - Usage:
     ```python
     async with manager.session() as session:
         result = await session.execute(select(User))
     ```
   - Guarantees:
     - Auto-rollback on errors
     - Session always closed properly
     - Transactions managed automatically

5. **Cleanup**:
   ```python
   async def close(self):
       await self._engine.dispose()
   ```
   - Shuts down connection pool when application exits

### 🧩 Why This Design?

1. **Safety First**  
   Context managers ensure resources are always released properly, even during errors.

2. **Async Optimization**  
   Uses SQLAlchemy's async features to prevent blocking.

3. **Separation of Concerns**

   - `connect()`: For raw SQL operations
   - `session()`: For ORM operations

4. **Test Friendly**  
   `create_all()`/`drop_all()` allow easy DB reset during testing.

### 💡 Real-World Analogy

Think of it like a car rental service:

- `init()` = Opening a rental location
- `connect()` = Renting a car (get keys → drive → return keys)
- `session()` = Renting a car with chauffeur (they handle driving)
- `close()` = Shutting down the rental location

This pattern is commonly used in FastAPI/async applications to safely manage database interactions.
