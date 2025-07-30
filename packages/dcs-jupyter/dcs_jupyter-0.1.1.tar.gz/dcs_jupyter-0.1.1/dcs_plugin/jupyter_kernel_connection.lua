SOCKET_ADDR = "127.0.0.1"
PORT = 8042

env.setErrorMessageBoxEnabled(false)
env.info("DCS Jupyter: Started lua plugin")
trigger.action.outText("DCS Jupyter: Started lua plugin", 2)

function connect()
    -- Use pre-initialized UDP socket from MissionScripting.lua
    local udp = _G['dcs_jupyter_udp']
    if not udp then
        error("DCS Jupyter UDP socket not initialized. Please check MissionScripting.lua patching.")
    end
    env.info("DCS Jupyter: Using pre-initialized UDP socket.")
    trigger.action.outText("DCS Jupyter: Using pre-initialized UDP socket.", 3)
    return udp
end

function execute_command(command_str, env)
    return xpcall(function ()
        local f = assert(loadstring("return " .. command_str, "=(zdcs)") or loadstring(command_str, "=(zdcs)"),
                         "syntax error, cannot load cmd '" .. command_str .. "'.")
        if env then
            f = setfenv(f, env)
        end
        return f()
    end, debug.traceback)
end

function process_request(udp_connection, env)
  return pcall(function ()
    local msg, addr, port = assert(udp_connection:receivefrom())
    local status, retval = execute_command(msg, env)
    assert(udp:sendto(tostring(retval), addr, port))
    return msg, status, retval
  end)
end


function timed_process_loop(udp, time)
    process_request(udp)
    return time + 0.1
end


udp = udp or connect()
timer.scheduleFunction(timed_process_loop, udp, timer.getTime() + 1)
