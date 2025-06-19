<?php

$baseUrl = 'http://127.0.0.1:27680/';

// 从查询参数中获取路径。
// 使用空值合并运算符 (??) 来处理 /mc 或 /mc/ 的情况，此时 'path' 不存在。
$path = $_GET['path'] ?? '';

// 拼接成完整的请求 URL
// 例如: http://127.0.0.1:27680/mcstatus
$targetUrl = $baseUrl . $path;

// 设置一个 stream context 来忽略 SSL 验证（如果目标是 HTTPS 且证书有问题）并获取响应头
// 对于本地 http 请求，这不是必需的，但这是一个好习惯
$context = stream_context_create([
    "ssl" => [
        "verify_peer" => false,
        "verify_peer_name" => false,
    ],
]);

// 使用 file_get_contents 获取目标 URL 的内容
// @ 符号可以抑制在请求失败时产生的警告，我们稍后会检查返回值
$content = @file_get_contents($targetUrl, false, $context);

if (isset($http_response_header) && is_array($http_response_header)) {
    foreach ($http_response_header as $header) {
        header($header); // 原样转发，例如 header('Content-Type: application/json');
    }
}

// header("Access-Control-Allow-Origin: *");

if ($content === false) {
    http_response_code(502);
    echo "Error: Could not forward request to the target service.";
} else {
    echo $content;
}

?>