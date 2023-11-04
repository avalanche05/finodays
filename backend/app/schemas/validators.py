def positive_number(x):
    from fastapi import HTTPException
    from fastapi import status
    if x <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid negative number")
    return x
