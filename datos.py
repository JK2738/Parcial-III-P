from sqlalchemy import Float, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = create_engine("sqlite:///zapateria.db", echo=False)


class Base(DeclarativeBase):
    pass


class Zapato(Base):
    __tablename__ = "zapatos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    modelo: Mapped[str] = mapped_column(String(100), nullable=False)
    talla: Mapped[int] = mapped_column(Integer, nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"Zapato(id={self.id}, modelo='{self.modelo}', talla={self.talla}, precio={self.precio})"


def inicializar_db() -> None:
    Base.metadata.create_all(engine)


def crear_zapato(modelo: str, talla: int, precio: float) -> Zapato:
    with Session(engine) as session:
        nuevo_zapato = Zapato(modelo=modelo, talla=talla, precio=precio)
        session.add(nuevo_zapato)
        session.commit()
        session.refresh(nuevo_zapato)
        return nuevo_zapato


def listar_zapatos() -> list[Zapato]:
    with Session(engine) as session:
        consulta = select(Zapato).order_by(Zapato.id)
        return list(session.scalars(consulta).all())


def buscar_zapato(zapato_id: int) -> Zapato | None:
    with Session(engine) as session:
        return session.get(Zapato, zapato_id)


def actualizar_precio(zapato_id: int, nuevo_precio: float) -> bool:
    with Session(engine) as session:
        zapato = session.get(Zapato, zapato_id)
        if zapato is None:
            return False
        zapato.precio = nuevo_precio
        session.commit()
        return True


def eliminar_zapato(zapato_id: int) -> bool:
    with Session(engine) as session:
        zapato = session.get(Zapato, zapato_id)
        if zapato is None:
            return False
        session.delete(zapato)
        session.commit()
        return True
