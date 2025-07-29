#!/bin/bash
# AIS - AI智能终端助手
# 智能安装脚本 - 统一推荐pipx安装
# 
# 推荐安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash
# 用户安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --user
# 系统安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --system
# 
# GitHub: https://github.com/kangvcar/ais

set -e  # 遇到错误立即退出

# 版本信息
AIS_VERSION="latest"
GITHUB_REPO="kangvcar/ais"

# 安装选项
NON_INTERACTIVE=0
INSTALL_MODE="auto"  # auto, user, system, container
SKIP_CHECKS=0

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印彩色消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检测系统环境
detect_environment() {
    if [ -n "${CONTAINER}" ] || [ -n "${container}" ] || [ -f /.dockerenv ]; then
        echo "container"
    elif [ "$EUID" -eq 0 ] && [ -n "$SUDO_USER" ]; then
        echo "sudo"
    elif [ "$EUID" -eq 0 ]; then
        echo "root"
    else
        echo "user"
    fi
}

# 安装pipx
install_pipx() {
    print_info "📦 安装pipx..."
    
    if command_exists pipx; then
        print_success "pipx已安装"
        return 0
    fi
    
    # 根据系统安装pipx
    if command_exists apt-get; then
        if [ "$(detect_environment)" = "user" ]; then
            sudo apt update && sudo apt install -y pipx
        else
            apt update && apt install -y pipx
        fi
    elif command_exists yum; then
        if [ "$(detect_environment)" = "user" ]; then
            sudo yum install -y pipx
        else
            yum install -y pipx
        fi
    elif command_exists brew; then
        brew install pipx
    else
        # 使用pip安装pipx
        if [ "$(detect_environment)" = "user" ]; then
            python3 -m pip install --user pipx
        else
            python3 -m pip install pipx
        fi
    fi
    
    # 确保pipx在PATH中
    python3 -m pipx ensurepath >/dev/null 2>&1 || true
    
    # 立即更新当前会话的PATH，使pipx可用
    export PATH="$HOME/.local/bin:$PATH"
    
    if command_exists pipx; then
        print_success "pipx安装成功"
    else
        print_error "pipx安装失败"
        return 1
    fi
}

# 自动设置Shell集成
setup_shell_integration_auto() {
    # 检测当前Shell
    local shell_name=""
    if [ -n "$ZSH_VERSION" ]; then
        shell_name="zsh"
    elif [ -n "$BASH_VERSION" ]; then
        shell_name="bash"
    else
        # 从SHELL环境变量推断
        case "$SHELL" in
            */zsh) shell_name="zsh" ;;
            */bash) shell_name="bash" ;;
            *) shell_name="bash" ;;  # 默认使用bash
        esac
    fi
    
    # 确定配置文件
    local config_file=""
    case "$shell_name" in
        "zsh")
            config_file="$HOME/.zshrc"
            ;;
        "bash")
            # 优先选择.bashrc，如果不存在则使用.bash_profile
            if [ -f "$HOME/.bashrc" ]; then
                config_file="$HOME/.bashrc"
            else
                config_file="$HOME/.bash_profile"
            fi
            ;;
    esac
    
    # 创建配置文件如果不存在
    if [ ! -f "$config_file" ]; then
        touch "$config_file"
    fi
    
    # 检查是否已经添加了AIS集成
    if grep -q "# START AIS INTEGRATION" "$config_file" 2>/dev/null; then
        print_info "Shell集成已存在，跳过设置"
        return 0
    fi
    
    # 获取AIS集成脚本路径（兼容用户级和系统级安装）
    local ais_script_path=""
    
    # 方法1：系统级pipx安装路径
    if [ -f "/opt/pipx/venvs/ais-terminal/lib/python*/site-packages/ais/shell/integration.sh" ]; then
        ais_script_path=$(echo /opt/pipx/venvs/ais-terminal/lib/python*/site-packages/ais/shell/integration.sh)
    fi
    
    # 方法2：用户级pipx安装路径
    if [ -z "$ais_script_path" ] && command_exists pipx; then
        local pipx_venv_path
        pipx_venv_path=$(pipx environment --value PIPX_LOCAL_VENVS 2>/dev/null || echo "$HOME/.local/share/pipx/venvs")
        local potential_path="$pipx_venv_path/ais-terminal/lib/python*/site-packages/ais/shell/integration.sh"
        if [ -f "$(echo $potential_path)" ]; then
            ais_script_path=$(echo $potential_path)
        fi
    fi
    
    # 方法3：通过Python查找
    if [ -z "$ais_script_path" ]; then
        ais_script_path=$(python3 -c "
try:
    import ais, os
    script_path = os.path.join(os.path.dirname(ais.__file__), 'shell', 'integration.sh')
    if os.path.exists(script_path):
        print(script_path)
except:
    pass
" 2>/dev/null)
    fi
    
    # 如果找到了脚本路径，添加到配置文件
    if [ -n "$ais_script_path" ] && [ -f "$ais_script_path" ]; then
        cat >> "$config_file" << EOF

# START AIS INTEGRATION
# AIS - AI 智能终端助手自动集成
if [ -f "$ais_script_path" ]; then
    source "$ais_script_path"
fi
# END AIS INTEGRATION
EOF
        print_success "已自动添加Shell集成到: $config_file"
        return 0
    else
        print_warning "无法找到AIS集成脚本，请稍后手动运行: ais setup"
        return 1
    fi
}

# 健康检查
health_check() {
    print_info "🔍 执行安装后健康检查..."
    
    # 检查ais命令
    if ! command_exists ais; then
        print_error "ais命令未找到"
        return 1
    fi
    
    # 检查版本
    VERSION=$(ais --version 2>/dev/null | head -n1) || {
        print_error "无法获取ais版本信息"
        return 1
    }
    
    print_success "ais命令可用: $VERSION"
    
    # 测试基本功能
    if ais config --help >/dev/null 2>&1; then
        print_success "基本功能测试通过"
    else
        print_warning "基本功能测试失败，但安装可能仍然成功"
    fi
    
    # 检查配置文件是否存在
    if [ -f "$HOME/.config/ais/config.toml" ]; then
        print_success "配置文件已生成"
    else
        print_info "首次运行时将自动生成配置文件"
    fi
    
    return 0
}

# 用户级安装
install_user_mode() {
    print_info "👤 开始用户级pipx安装..."
    
    # 安装pipx
    install_pipx || exit 1
    
    # 安装AIS
    print_info "📦 安装ais-terminal..."
    
    # 检查是否已安装并强制更新到最新版本
    if pipx list | grep -q "ais-terminal"; then
        print_info "发现已安装版本，更新到最新版本..."
        pipx upgrade ais-terminal
    else
        pipx install ais-terminal
    fi
    
    # 立即更新当前会话的PATH
    print_info "🔄 更新当前会话PATH..."
    export PATH="$HOME/.local/bin:$PATH"
    
    # 验证ais命令可用
    if ! command_exists ais; then
        print_error "安装后ais命令仍不可用，请检查安装"
        exit 1
    fi
    
    # 自动设置shell集成
    print_info "🔧 自动设置shell集成..."
    if setup_shell_integration_auto; then
        print_success "Shell集成设置完成"
    else
        print_warning "Shell集成自动设置失败，稍后运行: ais setup"
    fi
    
    # 简化的健康检查
    print_info "🔍 验证安装..."
    
    # 刷新pipx并获取版本信息
    # 确保pipx环境更新
    pipx ensurepath >/dev/null 2>&1 || true
    hash -r 2>/dev/null || true  # 刷新命令缓存
    
    VERSION=$(ais --version 2>/dev/null | head -n1) || {
        print_error "安装失败：ais命令不可用"
        exit 1
    }
    
    print_success "🎉 AIS安装完成！版本: $VERSION"
    
    # 检测配置文件并提供激活指导
    local config_file=""
    if [ -n "$ZSH_VERSION" ] && [ -f "$HOME/.zshrc" ]; then
        config_file="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ] && [ -f "$HOME/.bashrc" ]; then
        config_file="$HOME/.bashrc"
    elif [ -f "$HOME/.bashrc" ]; then
        config_file="$HOME/.bashrc"
    elif [ -f "$HOME/.bash_profile" ]; then
        config_file="$HOME/.bash_profile"
    fi
    
    echo
    print_warning "🔧 重要：要启用自动错误分析，请执行以下命令之一："
    if [ -n "$config_file" ]; then
        print_info "   source $config_file"
        print_info "   或者重新打开终端"
    else
        print_info "   重新打开终端"
    fi
    
    echo
    print_info "🚀 快速测试: ais ask '你好'"
}

# 系统级安装
install_system_mode() {
    print_info "🏢 开始系统级pipx安装..."
    
    # 安装pipx
    install_pipx || exit 1
    
    # 创建系统级pipx环境
    export PIPX_HOME=/opt/pipx
    export PIPX_BIN_DIR=/usr/local/bin
    
    # 安装AIS
    print_info "📦 安装ais-terminal到系统位置..."
    
    # 检查是否已安装并强制更新到最新版本
    if [ "$(detect_environment)" = "user" ]; then
        if sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx list | grep -q "ais-terminal"; then
            print_info "发现已安装版本，更新到最新版本..."
            sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx upgrade ais-terminal
        else
            sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install ais-terminal
        fi
    else
        if pipx list | grep -q "ais-terminal"; then
            print_info "发现已安装版本，更新到最新版本..."
            pipx upgrade ais-terminal
        else
            pipx install ais-terminal
        fi
    fi
    
    # 确保所有用户可访问
    if [ "$(detect_environment)" = "user" ]; then
        sudo chmod +x /usr/local/bin/ais 2>/dev/null || true
    else
        chmod +x /usr/local/bin/ais 2>/dev/null || true
    fi
    
    # 验证安装
    VERSION=$(ais --version 2>/dev/null | head -n1) || {
        print_error "系统级安装失败：ais命令不可用"
        exit 1
    }
    
    print_success "🎉 AIS系统级安装完成！版本: $VERSION"
    
    # 系统级安装：配置全局Shell集成，让所有用户都能自动启用
    print_info "🔧 配置全局Shell集成..."
    
    # 获取AIS集成脚本路径
    local ais_script_path=""
    if [ -f "/opt/pipx/venvs/ais-terminal/lib/python*/site-packages/ais/shell/integration.sh" ]; then
        ais_script_path=$(echo /opt/pipx/venvs/ais-terminal/lib/python*/site-packages/ais/shell/integration.sh)
    else
        ais_script_path=$(python3 -c "
try:
    import ais, os
    script_path = os.path.join(os.path.dirname(ais.__file__), 'shell', 'integration.sh')
    if os.path.exists(script_path):
        print(script_path)
except:
    pass
" 2>/dev/null)
    fi
    
    if [ -n "$ais_script_path" ] && [ -f "$ais_script_path" ]; then
        # 创建全局Shell集成配置
        local global_config="/etc/profile.d/ais.sh"
        
        if [ "$(detect_environment)" = "user" ]; then
            # 非root用户需要sudo
            sudo tee "$global_config" > /dev/null << EOF
#!/bin/bash
# AIS - AI 智能终端助手全局集成
# 自动为所有用户启用AIS Shell集成

# 检查AIS集成脚本是否存在
if [ -f "$ais_script_path" ]; then
    # 只在交互式shell中加载
    if [[ \$- == *i* ]]; then
        source "$ais_script_path"
    fi
fi
EOF
            sudo chmod +x "$global_config"
        else
            # root用户直接创建
            cat > "$global_config" << EOF
#!/bin/bash
# AIS - AI 智能终端助手全局集成
# 自动为所有用户启用AIS Shell集成

# 检查AIS集成脚本是否存在
if [ -f "$ais_script_path" ]; then
    # 只在交互式shell中加载
    if [[ \$- == *i* ]]; then
        source "$ais_script_path"
    fi
fi
EOF
            chmod +x "$global_config"
        fi
        
        print_success "已配置全局Shell集成: $global_config"
    else
        print_warning "无法找到AIS集成脚本，全局配置失败"
    fi
    
    # 同时为当前用户配置（确保立即可用）
    print_info "🔧 为当前用户配置Shell集成..."
    if setup_shell_integration_auto; then
        print_success "当前用户Shell集成设置完成"
    else
        print_warning "当前用户Shell集成自动设置失败"
    fi
    
    echo
    print_info "💡 所有用户都可以使用ais命令"
    print_success "🎯 系统级安装和全局配置已完全完成！"
    echo
    print_warning "🔧 重要：请重新打开终端或重新登录以启用自动分析"
    print_info "   所有用户（包括新用户）都将自动启用AIS功能"
    echo
    print_info "🚀 重新打开终端后，任何用户都可以直接使用："
    print_info "   ais config       # 查看和配置AI服务"
    print_info "   ais ask '你好'    # 快速测试"
    print_info "   任何错误命令     # 将自动显示AI分析"
}

# 容器化安装
install_container_mode() {
    print_info "🐳 开始容器化安装..."
    
    # 在容器中使用简单的pip安装
    print_info "📦 在容器中安装ais-terminal..."
    python3 -m pip install --break-system-packages ais-terminal
    
    # 创建全局可用的ais命令
    if [ -w "/usr/local/bin" ]; then
        cat > /usr/local/bin/ais << 'EOF'
#!/usr/bin/env python3
import sys
from ais.cli.main import main
if __name__ == '__main__':
    sys.exit(main())
EOF
        chmod +x /usr/local/bin/ais
    fi
    
    print_success "✅ 容器化安装完成！"
    print_info "💡 容器内直接使用: ais --version"
}

# 主安装函数
main() {
    echo "================================================"
    echo "         AIS - AI 智能终端助手 安装器"
    echo "================================================"
    echo "版本: $AIS_VERSION"
    echo "GitHub: https://github.com/$GITHUB_REPO"
    echo
    
    ENV=$(detect_environment)
    print_info "🔍 检测到环境: $ENV"
    
    # 自动选择最佳安装模式
    if [ "$INSTALL_MODE" = "auto" ]; then
        case "$ENV" in
            "container")
                INSTALL_MODE="container"
                print_info "🐳 容器环境：使用容器化安装"
                ;;
            "root"|"sudo")
                INSTALL_MODE="system"
                print_info "🏢 管理员环境：使用系统级pipx安装"
                ;;
            "user")
                INSTALL_MODE="user"
                print_info "👤 用户环境：使用用户级pipx安装"
                ;;
        esac
    fi
    
    # 执行对应的安装模式
    case "$INSTALL_MODE" in
        "user")
            install_user_mode
            ;;
        "system")
            install_system_mode
            ;;
        "container")
            install_container_mode
            ;;
        *)
            print_error "未知的安装模式: $INSTALL_MODE"
            exit 1
            ;;
    esac
    
    # 健康检查已在各安装模式中完成
}

# 处理命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --user)
            INSTALL_MODE="user"
            shift
            ;;
        --system)
            INSTALL_MODE="system"
            shift
            ;;
        --container)
            INSTALL_MODE="container"
            shift
            ;;
        --non-interactive)
            NON_INTERACTIVE=1
            shift
            ;;
        --skip-checks)
            SKIP_CHECKS=1
            shift
            ;;
        --help)
            echo "AIS 智能安装脚本"
            echo
            echo "用法: $0 [选项]"
            echo
            echo "安装模式:"
            echo "  (无参数)          自动检测环境并选择最佳安装方式"
            echo "  --user           用户级pipx安装（推荐个人使用）"
            echo "  --system         系统级pipx安装（推荐多用户环境）"
            echo "  --container      容器化安装（适用于Docker等）"
            echo
            echo "其他选项:"
            echo "  --non-interactive  非交互模式，适用于CI/CD环境"
            echo "  --skip-checks      跳过安装后健康检查"
            echo "  --help            显示此帮助信息"
            echo
            echo "安装示例:"
            echo "  个人安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash"
            echo "  系统安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --system"
            echo "  容器安装: curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --container"
            echo
            echo "💡 推荐使用pipx进行安装，提供最佳的安全性和可维护性"
            exit 0
            ;;
        *)
            print_error "未知选项: $1"
            print_info "使用 --help 查看帮助"
            exit 1
            ;;
    esac
done

# 运行主函数
main