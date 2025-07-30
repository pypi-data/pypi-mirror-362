"""
核心功能测试
"""

import pytest
from unittest.mock import Mock, patch
import requests
import socket

from net_utils_ky.core import NetworkUtils, HTTPClient, NetworkChecker, PortScanner
from net_utils_ky.exceptions import HTTPRequestError


class TestHTTPClient:
    """HTTP客户端测试"""
    
    def test_init(self):
        """测试初始化"""
        client = HTTPClient()
        assert client.timeout == (5, 30)
        assert client.proxy is None
        assert client.retries == 3
    
    def test_init_with_params(self):
        """测试带参数的初始化"""
        client = HTTPClient(
            timeout=(10, 60),
            proxy="http://proxy.example.com:8080",
            retries=5,
            headers={"User-Agent": "test"}
        )
        assert client.timeout == (10, 60)
        assert client.proxy == "http://proxy.example.com:8080"
        assert client.retries == 5
        assert client.headers == {"User-Agent": "test"}
    
    @patch('requests.Session')
    def test_get_success(self, mock_session):
        """测试GET请求成功"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        client = HTTPClient()
        response = client.get("https://example.com")
        
        assert response == mock_response
        mock_session_instance.get.assert_called_once()
    
    @patch('requests.Session')
    def test_get_failure(self, mock_session):
        """测试GET请求失败"""
        mock_session_instance = Mock()
        mock_session_instance.get.side_effect = requests.exceptions.RequestException("Connection error")
        mock_session.return_value = mock_session_instance
        
        client = HTTPClient()
        
        with pytest.raises(HTTPRequestError):
            client.get("https://example.com")


class TestNetworkChecker:
    """网络检测器测试"""
    
    def test_init(self):
        """测试初始化"""
        checker = NetworkChecker()
        assert checker.timeout == 5
    
    def test_init_with_timeout(self):
        """测试带超时的初始化"""
        checker = NetworkChecker(timeout=10)
        assert checker.timeout == 10
    
    @patch('requests.get')
    def test_is_connected_success(self, mock_get):
        """测试连接检测成功"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        checker = NetworkChecker()
        result = checker.is_connected()
        
        assert result is True
    
    @patch('requests.get')
    def test_is_connected_failure(self, mock_get):
        """测试连接检测失败"""
        mock_get.side_effect = Exception("Connection error")
        
        checker = NetworkChecker()
        result = checker.is_connected()
        
        assert result is False
    
    @patch('socket.gethostbyname')
    def test_dns_works_success(self, mock_gethostbyname):
        """测试DNS解析成功"""
        mock_gethostbyname.return_value = "8.8.8.8"
        
        checker = NetworkChecker()
        result = checker.dns_works()
        
        assert result is True
    
    @patch('socket.gethostbyname')
    def test_dns_works_failure(self, mock_gethostbyname):
        """测试DNS解析失败"""
        mock_gethostbyname.side_effect = socket.gaierror("DNS resolution failed")
        
        checker = NetworkChecker()
        result = checker.dns_works()
        
        assert result is False


class TestPortScanner:
    """端口扫描器测试"""
    
    def test_init(self):
        """测试初始化"""
        scanner = PortScanner()
        assert scanner.timeout == 1.0
    
    def test_init_with_timeout(self):
        """测试带超时的初始化"""
        scanner = PortScanner(timeout=2.0)
        assert scanner.timeout == 2.0
    
    @patch('socket.socket')
    def test_is_port_open_success(self, mock_socket):
        """测试端口开放检测成功"""
        mock_sock = Mock()
        mock_sock.connect_ex.return_value = 0
        mock_socket.return_value = mock_sock
        
        scanner = PortScanner()
        result = scanner.is_port_open("example.com", 80)
        
        assert result is True
        mock_sock.close.assert_called_once()
    
    @patch('socket.socket')
    def test_is_port_open_failure(self, mock_socket):
        """测试端口开放检测失败"""
        mock_sock = Mock()
        mock_sock.connect_ex.return_value = 1
        mock_socket.return_value = mock_sock
        
        scanner = PortScanner()
        result = scanner.is_port_open("example.com", 80)
        
        assert result is False
        mock_sock.close.assert_called_once()
    
    def test_scan_ports(self):
        """测试端口扫描"""
        scanner = PortScanner()
        
        with patch.object(scanner, 'is_port_open') as mock_is_open:
            mock_is_open.side_effect = [True, False, True]
            
            result = scanner.scan_ports("example.com", [80, 443, 8080])
            
            assert result == [80, 8080]
            assert mock_is_open.call_count == 3
    
    def test_scan_common_ports(self):
        """测试常见端口扫描"""
        scanner = PortScanner()
        
        with patch.object(scanner, 'is_port_open') as mock_is_open:
            mock_is_open.return_value = True
            
            result = scanner.scan_common_ports("example.com")
            
            # 检查是否扫描了常见端口
            assert len(result) > 0
            assert all(result.values())  # 所有端口都应该是开放的


class TestNetworkUtils:
    """网络工具主类测试"""
    
    def test_init(self):
        """测试初始化"""
        utils = NetworkUtils()
        assert utils.http_client is not None
        assert utils.network_checker is not None
        assert utils.port_scanner is not None
    
    def test_init_with_params(self):
        """测试带参数的初始化"""
        utils = NetworkUtils(
            timeout=(10, 60),
            proxy="http://proxy.example.com:8080",
            retries=5
        )
        assert utils.http_client.timeout == (10, 60)
        assert utils.http_client.proxy == "http://proxy.example.com:8080"
        assert utils.http_client.retries == 5
    
    def test_get_delegation(self):
        """测试GET请求委托"""
        utils = NetworkUtils()
        
        with patch.object(utils.http_client, 'get') as mock_get:
            mock_response = Mock()
            mock_get.return_value = mock_response
            
            result = utils.get("https://example.com")
            
            assert result == mock_response
            mock_get.assert_called_once_with("https://example.com")
    
    def test_is_connected_delegation(self):
        """测试连接检测委托"""
        utils = NetworkUtils()
        
        with patch.object(utils.network_checker, 'is_connected') as mock_check:
            mock_check.return_value = True
            
            result = utils.is_connected()
            
            assert result is True
            mock_check.assert_called_once()
    
    def test_is_port_open_delegation(self):
        """测试端口检测委托"""
        utils = NetworkUtils()
        
        with patch.object(utils.port_scanner, 'is_port_open') as mock_scan:
            mock_scan.return_value = True
            
            result = utils.is_port_open("example.com", 80)
            
            assert result is True
            mock_scan.assert_called_once_with("example.com", 80) 