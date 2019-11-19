class BasePermission
{
    isAuthenticated(req)
    {
        let headers = req.headers.authorization;
        if(!headers)
        {
            return false;
        }
        return true;
    }
}

exports.BasePermission = BasePermission;
