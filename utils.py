# Utilitários para o Bot de Controle Financeiro

import re
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from config import CURRENCY_SYMBOL, DATE_FORMAT, DATA_DIR


def ensure_data_dir():
    """Garante que o diretório de dados existe."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def parse_value(value_str: str) -> Optional[float]:
    """
    Converte string de valor para float, aceitando vírgula ou ponto como separador decimal.
    
    Args:
        value_str: String contendo o valor (ex: "150,50" ou "150.50")
        
    Returns:
        Float do valor ou None se inválido
    """
    if not value_str:
        return None
    
    # Remove espaços e substitui vírgula por ponto
    clean_value = value_str.strip().replace(',', '.')
    
    # Verifica se é um número válido
    if re.match(r'^\d+(\.\d{1,2})?$', clean_value):
        return float(clean_value)
    
    return None


def parse_date(date_str: str) -> str:
    """
    Converte string de data para formato padrão ou retorna data atual.
    
    Args:
        date_str: String da data (ex: "12/08/2025") ou None
        
    Returns:
        String da data no formato padrão
    """
    if not date_str:
        return datetime.now().strftime(DATE_FORMAT)
    
    # Tenta diferentes formatos de data
    formats = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']
    
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            return parsed_date.strftime(DATE_FORMAT)
        except ValueError:
            continue
    
    # Se não conseguir parsear, usa data atual
    return datetime.now().strftime(DATE_FORMAT)


def format_currency(value: float) -> str:
    """
    Formata valor como moeda brasileira.
    
    Args:
        value: Valor numérico
        
    Returns:
        String formatada (ex: "R$ 1.234,56")
    """
    return f"{CURRENCY_SYMBOL} {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def load_json_data(filename: str) -> Dict[str, Any]:
    """
    Carrega dados de arquivo JSON.
    
    Args:
        filename: Nome do arquivo
        
    Returns:
        Dicionário com os dados ou dicionário vazio se arquivo não existir
    """
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    return {}


def save_json_data(filename: str, data: Dict[str, Any]):
    """
    Salva dados em arquivo JSON.
    
    Args:
        filename: Nome do arquivo
        data: Dados para salvar
    """
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"Erro ao salvar dados: {e}")


def calculate_balance(lancamentos: List[Dict[str, Any]]) -> float:
    """
    Calcula o saldo baseado na lista de lançamentos.
    
    Args:
        lancamentos: Lista de lançamentos
        
    Returns:
        Saldo atual
    """
    balance = 0.0
    
    for lancamento in lancamentos:
        valor = lancamento.get('valor', 0.0)
        if lancamento.get('tipo') == 'entrada':
            balance += valor
        elif lancamento.get('tipo') == 'saida':
            balance -= valor
    
    return balance


def get_month_summary(lancamentos: List[Dict[str, Any]], month: Optional[str] = None) -> Dict[str, float]:
    """
    Calcula resumo do mês especificado ou atual.
    
    Args:
        lancamentos: Lista de lançamentos
        month: Mês no formato "MM/YYYY" ou None para mês atual
        
    Returns:
        Dicionário com entradas, saídas e saldo do mês
    """
    if not month:
        month = datetime.now().strftime("%m/%Y")
    
    entradas = 0.0
    saidas = 0.0
    
    for lancamento in lancamentos:
        data = lancamento.get('data', '')
        if data.endswith(month):
            valor = lancamento.get('valor', 0.0)
            if lancamento.get('tipo') == 'entrada':
                entradas += valor
            elif lancamento.get('tipo') == 'saida':
                saidas += valor
    
    return {
        'entradas': entradas,
        'saidas': saidas,
        'saldo': entradas - saidas
    }


def format_lancamento(lancamento: Dict[str, Any], include_author: bool = False) -> str:
    """
    Formata um lançamento para exibição.
    
    Args:
        lancamento: Dicionário do lançamento
        include_author: Se deve incluir o autor (para grupos do Telegram)
        
    Returns:
        String formatada do lançamento
    """
    tipo_symbol = "➕" if lancamento.get('tipo') == 'entrada' else "➖"
    valor = format_currency(lancamento.get('valor', 0.0))
    descricao = lancamento.get('descricao', '')
    data = lancamento.get('data', '')
    
    result = f"{tipo_symbol} {valor}"
    
    if descricao:
        result += f" — {descricao}"
    
    if data:
        result += f" ({data})"
    
    if include_author and 'autor' in lancamento:
        result = f"{lancamento['autor']} {result}"
    
    return result

