#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from typing import Optional, List, Dict
from abc import ABC, abstractmethod
from re import fullmatch


class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name: str = name
        self.price: float = price

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError:
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania


class Server(ABC):
    n_max_returned_entries: int = 3

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        products = self.get_products()
        result = []
        for el in products:
            if el.name == re.fullmatch(r"[a-zA-Z]{"+str(n_letters)+"}[0-9]{2,3}"):
                result.append(el)
        if len(result) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError
        return result.sort(key=lambda x: x.price)

    @abstractmethod
    def get_products(self) -> List[Product]:
        raise NotImplementedError


class ListServer(Server):
    def __init__(self, products: List[Product]) -> None:
        self.products: List[Product] = products

    def get_products(self) -> List[Product]:
        return self.products


class MapServer(Server):
    def __init__(self, products: List[Product]) -> None:
        self.products: Dict[str, Product] = {el.name: el for el in products}

    def get_products(self) -> List[Product]:
        return list(self.products.values())


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server: Server) -> None:
        pass

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()